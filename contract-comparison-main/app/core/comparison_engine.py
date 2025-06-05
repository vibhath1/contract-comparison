# comparison_engine.py
import difflib
import language_tool_python
import os
from typing import List, Dict, Any, Union
from date_comparison import compare_date_references  # Import the new date comparison module
from app.core.semantic_model import get_semantic_model
from formatting_engine import (
    extract_formatting_docx,
    extract_formatting_pdf,
    compare_formatting
)
from visual_engine import compare_visual_elements

try:
    from sentence_transformers import util
except ImportError:
    util = None
    print("Warning: sentence-transformers 'util' module not available. Semantic diff disabled.")

try:
    import nltk
    nltk.data.find('tokenizers/punkt')
except LookupError:
    import nltk
    nltk.download('punkt')

# Initialize SentenceTransformer model globally with fallback handling
try:
    model = get_semantic_model("paraphrase-MiniLM-L6-v2")
except Exception as e:
    print(f"Warning: Could not load semantic model: {e}")
    model = None


def sentence_tokenize(text: str) -> List[str]:
    """
    Tokenize text into sentences using nltk.sent_tokenize for better accuracy than naive split.
    """
    if not text:
        return []
    return nltk.sent_tokenize(text)


def get_text_diff_semantic(text1: str, text2: str) -> Union[List[Dict[str, Any]], List[Dict[str, str]]]:
    """
    Perform semantic sentence-level comparison between two texts using sentence-transformers.
    Returns a list of dicts describing differences where similarity is below threshold.
    Falls back to a simple warning if model or util is not available.
    """
    if not model or util is None:
        return [{"note": "Semantic model or utility unavailable. Semantic diff skipped."}]

    sentences1 = [s.strip() for s in sentence_tokenize(text1) if s.strip()]
    sentences2 = [s.strip() for s in sentence_tokenize(text2) if s.strip()]

    if not sentences1 or not sentences2:
        return [{"note": "One or both documents are empty or could not be processed for semantic diff."}]

    try:
        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)

        # Ensure embeddings are on the same device
        if embeddings1.device != embeddings2.device:
            embeddings2 = embeddings2.to(embeddings1.device)

        results = []
        for i, s1 in enumerate(sentences1):
            emb1_i = embeddings1[i]
            if emb1_i.ndim == 0:
                continue
            if emb1_i.ndim == 1:
                emb1_i = emb1_i.unsqueeze(0)

            sim_scores = util.cos_sim(emb1_i, embeddings2)
            if sim_scores.numel() == 0:
                max_score_val, max_idx_val = 0.0, 0
            else:
                max_score, max_idx = sim_scores[0].max(dim=0)
                max_score_val, max_idx_val = max_score.item(), max_idx.item()

            # Threshold for "meaning may differ"
            if max_score_val < 0.75:
                matched_sentence = sentences2[max_idx_val] if max_idx_val < len(sentences2) else "N/A"
                results.append({
                    "original_sentence": s1,
                    "matched_sentence": matched_sentence,
                    "similarity_score": round(float(max_score_val), 4),
                    "note": "Meaning may differ"
                })
        return results
    except Exception as e:
        print(f"Error during semantic diff computation: {e}")
        return [{"note": f"Error computing semantic diff: {e}"}]


def get_text_diff(text1: str, text2: str) -> str:
    """
    Generate a unified diff string between two texts using difflib.
    """
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()
    diff = difflib.unified_diff(text1_lines, text2_lines,
                                fromfile='Document 1', tofile='Document 2', lineterm='')
    return "\n".join(diff)


def get_word_level_diff(text1: str, text2: str) -> List[Dict[str, Any]]:
    """
    Perform word-level comparison between two texts.
    Returns a structured JSON diff for frontend highlighting.
    """
    result = []
    words1 = text1.split()
    words2 = text2.split()
    sm = difflib.SequenceMatcher(None, words1, words2)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace":
            result.append({
                "type": "replaced",
                "old_text": " ".join(words1[i1:i2]),
                "new_text": " ".join(words2[j1:j2])
            })
        elif tag == "delete":
            result.append({
                "type": "removed",
                "text": " ".join(words1[i1:i2])
            })
        elif tag == "insert":
            result.append({
                "type": "added",
                "text": " ".join(words2[j1:j2])
            })
    return result


def get_grammar_issues(text: str) -> List[Dict[str, Any]]:
    """
    Use language_tool_python to check grammar issues in text.
    Returns a list of dicts with issue details.
    """
    try:
        tool = language_tool_python.LanguageTool('en-US')
    except Exception as e:
        print(f"Error initializing LanguageTool: {e}. Grammar check will be skipped.")
        return [{
            "message": "Grammar check skipped due to LanguageTool initialization error.",
            "suggestions": [],
            "offset": 0,
            "length": 0,
            "context": ""
        }]

    try:
        matches = tool.check(text)
        return [
            {
                "message": match.message,
                "suggestions": match.replacements,
                "offset": match.offset,
                "length": match.errorLength,
                "context": match.context
            }
            for match in matches
        ]
    except Exception as e:
        print(f"Error during grammar checking: {e}")
        return [{
            "message": f"Grammar check failed: {e}",
            "suggestions": [],
            "offset": 0,
            "length": 0,
            "context": ""
        }]


def compare_documents(text1: str, text2: str, file1_path: str, file2_path: str, yolo_model_path: str) -> Dict[str, Any]:
    """
    Main function to compare two documents with multiple analysis layers:
    - semantic text difference
    - grammar issues
    - formatting difference
    - visual element comparison (if PDF or images)
    - date references comparison

    Returns a dictionary summarizing all comparison results.
    """
    diff_output_semantic = get_text_diff_semantic(text1, text2)
    structured_word_diff = get_word_level_diff(text1, text2)

    grammar1 = get_grammar_issues(text1) if text1 else []
    grammar2 = get_grammar_issues(text2) if text2 else []

    ext1 = os.path.splitext(file1_path)[1].lower()
    ext2 = os.path.splitext(file2_path)[1].lower()

    try:
        fmt1 = extract_formatting_docx(file1_path) if ext1 == ".docx" else extract_formatting_pdf(file1_path)
    except Exception as e:
        print(f"Error extracting formatting from {file1_path}: {e}")
        fmt1 = []

    try:
        fmt2 = extract_formatting_docx(file2_path) if ext2 == ".docx" else extract_formatting_pdf(file2_path)
    except Exception as e:
        print(f"Error extracting formatting from {file2_path}: {e}")
        fmt2 = []

    formatting_diff = []
    try:
        formatting_diff = compare_formatting(fmt1, fmt2)
    except Exception as e:
        print(f"Error comparing formatting: {e}")

    visual_result = {"notes": ["Visual comparison not applicable or skipped for the given file types."]}
    visual_comparison_types = [".pdf", ".png", ".jpg", ".jpeg"]

    if ext1 in visual_comparison_types and ext2 in visual_comparison_types:
        try:
            visual_result = compare_visual_elements(file1_path, file2_path, yolo_model_path=yolo_model_path)
        except Exception as e:
            print(f"Error during visual comparison: {e}")
            visual_result = {"notes": [f"Visual comparison error: {e}"]}
    else:
        notes_list = []
        if ext1 not in visual_comparison_types:
            notes_list.append(f"Document 1 ('{os.path.basename(file1_path)}' type: {ext1}) is not a PDF/Image.")
        if ext2 not in visual_comparison_types:
            notes_list.append(f"Document 2 ('{os.path.basename(file2_path)}' type: {ext2}) is not a PDF/Image.")
        if not notes_list:
            notes_list.append("Visual comparison skipped as one or both files are not PDF/Image types.")
        else:
            notes_list.append("Therefore, visual comparison was skipped.")
        visual_result = {"notes": notes_list}

    try:
        date_comparison = compare_date_references(text1, text2)
    except Exception as e:
        print(f"Error during date comparison: {e}")
        date_comparison = {"notes": [f"Date comparison error: {e}"]}

    return {
        "text_diff_semantic": diff_output_semantic,
        "text_diff_structured": structured_word_diff,
        "grammar_issues_doc1": grammar1,
        "grammar_issues_doc2": grammar2,
        "formatting_diff": formatting_diff,
        "visual_comparison": visual_result,
        "date_comparison": date_comparison
    }
