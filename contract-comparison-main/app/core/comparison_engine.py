import difflib
import language_tool_python


from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")



def get_text_diff_semantic(text1: str, text2: str) -> list:
    sentences1 = [s.strip() for s in text1.split('.') if s.strip()]
    sentences2 = [s.strip() for s in text2.split('.') if s.strip()]

    if not sentences1 or not sentences2:
        return [{"note": "One or both documents are empty or could not be processed."}]

    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    results = []
    for i, s1 in enumerate(sentences1):
        sim_scores = util.cos_sim(embeddings1[i], embeddings2)
        max_score, max_idx = sim_scores[0].max(0)

        if max_score < 0.75:
            results.append({
                "original_sentence": s1,
                "matched_sentence": sentences2[max_idx],
                "similarity_score": round(float(max_score), 4),
                "note": "Meaning may differ"
            })

    return results


from app.core.formatting_engine import (
    extract_formatting_docx,
    extract_formatting_pdf,
    compare_formatting
)

from app.core.visual_engine import (
    compare_visual_elements
)

def get_text_diff(text1: str, text2: str) -> str:
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()
    diff = difflib.unified_diff(text1_lines, text2_lines, fromfile='Document 1', tofile='Document 2', lineterm='')
    return "\n".join(diff)

def get_grammar_issues(text: str) -> list:
    tool = language_tool_python.LanguageTool('en-US')
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

def compare_documents(text1: str, text2: str, file1_path: str, file2_path: str) -> dict:
    # Compare text and grammar
    diff_output = get_text_diff_semantic(text1, text2)
    grammar1 = get_grammar_issues(text1)
    grammar2 = get_grammar_issues(text2)

    # Extract formatting
    ext1 = file1_path.lower().split('.')[-1]
    ext2 = file2_path.lower().split('.')[-1]

    fmt1 = extract_formatting_docx(file1_path) if ext1 == "docx" else extract_formatting_pdf(file1_path)
    fmt2 = extract_formatting_docx(file2_path) if ext2 == "docx" else extract_formatting_pdf(file2_path)
    formatting_diff = compare_formatting(fmt1, fmt2)

    # Visual similarity (PDF only)
    visual_result = {}
    if ext1 == "pdf" and ext2 == "pdf":
        visual_result = compare_visual_elements(file1_path, file2_path)

    return {
        "text_diff": diff_output,
        "grammar_issues_doc1": grammar1,
        "grammar_issues_doc2": grammar2,
        "formatting_diff": formatting_diff,
        "visual_comparison": visual_result
    }
