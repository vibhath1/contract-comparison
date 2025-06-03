from docx import Document
import pdfplumber
from typing import List, Dict, Any

def extract_formatting_docx(path: str) -> List[Dict[str, Any]]:
    """
    Extracts a list of formatting metadata for each text run in a DOCX.
    Each entry contains the run text, font name, size, bold/italic, and alignment.
    """
    doc = Document(path)
    formatted_runs = []
    for para in doc.paragraphs:
        align = para.alignment  # None, 0=left, 1=center, 2=right, 3=justify
        for run in para.runs:
            fmt = {
                "text": run.text,
                "font_name": run.font.name,
                "font_size": run.font.size.pt if run.font.size else None,
                "bold": run.font.bold,
                "italic": run.font.italic,
                "alignment": align,
            }
            formatted_runs.append(fmt)
    return formatted_runs

def extract_formatting_pdf(path: str) -> List[Dict[str, Any]]:
    """
    Extract a list of formatting metadata for each text chunk in a PDF using pdfplumber.
    Each entry includes the text, font size, font name, and position.
    """
    formatted_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for obj in page.extract_words(extra_attrs=[
                "fontname", "size", "x0", "top", "x1", "bottom"
            ]):
                formatted_chunks.append({
                    "text": obj["text"],
                    "font_name": obj.get("fontname"),
                    "font_size": obj.get("size"),
                    "x0": obj.get("x0"),
                    "top": obj.get("top"),
                })
    return formatted_chunks

def compare_formatting(doc1_fmt: List[Dict], doc2_fmt: List[Dict]) -> Dict[str, List]:
    """
    Compare two formatting lists. Returns:
      - added_formats: runs/chunks present in doc2 but not in doc1
      - removed_formats: runs/chunks in doc1 but not in doc2
      - changed_formats: same text but different attributes
    """
    added, removed, changed = [], [], []
    idx1 = { item["text"]: item for item in doc1_fmt if item.get("text") }
    idx2 = { item["text"]: item for item in doc2_fmt if item.get("text") }

    # Added or changed in doc2
    for text, fmt2 in idx2.items():
        fmt1 = idx1.get(text)
        if not fmt1:
            added.append(fmt2)
        else:
            common_keys = set(fmt1.keys()).intersection(set(fmt2.keys()))
            diffs = {k: (fmt1.get(k), fmt2.get(k)) for k in common_keys if fmt1.get(k) != fmt2.get(k)}
            if diffs:
                changed.append({"text": text, "differences": diffs})

    # Removed in doc2
    for text, fmt1 in idx1.items():
        if text not in idx2:
            removed.append(fmt1)

    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
