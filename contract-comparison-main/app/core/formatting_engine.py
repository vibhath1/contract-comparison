#formatting_engine.py

from typing import List, Dict, Any
import os
import logging

from docx import Document
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Configure logging instead of print for better production suitability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIN_TEXT_LENGTH = 2  # Minimum text length to consider for formatting (filters out very short runs/punctuation)


def extract_formatting_docx(path: str) -> List[Dict[str, Any]]:
    """
    Extract formatting metadata from DOCX file.
    Each entry contains text, font name, size (pt), bold, italic, and alignment.
    Filters out very short or empty text runs.
    """
    formatted_runs = []
    try:
        doc = Document(path)
        for para in doc.paragraphs:
            align = para.alignment  # None, 0=left, 1=center, 2=right, 3=justify
            for run in para.runs:
                text = run.text.strip()
                if len(text) < MIN_TEXT_LENGTH:
                    continue
                fmt = {
                    "text": text,
                    "font_name": run.font.name if run.font.name else None,
                    "font_size": run.font.size.pt if run.font.size else None,
                    "bold": run.font.bold,
                    "italic": run.font.italic,
                    "alignment": align,
                }
                formatted_runs.append(fmt)
    except Exception as e:
        logger.error(f"[extract_formatting_docx] Error: {e}")
    return formatted_runs


def extract_formatting_pdf(path: str) -> List[Dict[str, Any]]:
    """
    Extract formatting metadata from native PDF using pdfplumber.
    Returns list of text chunks with font name, font size, and position.
    Filters out empty or very short text chunks.
    """
    formatted_chunks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(extra_attrs=[
                    "fontname", "size", "x0", "top", "x1", "bottom"
                ])
                for obj in words:
                    text = obj.get("text", "").strip()
                    if len(text) < MIN_TEXT_LENGTH:
                        continue
                    formatted_chunks.append({
                        "text": text,
                        "font_name": obj.get("fontname"),
                        "font_size": obj.get("size"),
                        "x0": obj.get("x0"),
                        "top": obj.get("top"),
                        "x1": obj.get("x1"),
                        "bottom": obj.get("bottom"),
                    })
    except Exception as e:
        logger.error(f"[extract_formatting_pdf] Error: {e}")
    return formatted_chunks


def extract_formatting_scanned_pdf(path: str) -> List[Dict[str, Any]]:
    """
    For scanned PDFs: convert pages to images, run OCR,
    extract text with bounding boxes as approximate formatting info.
    Filters out short/empty text.
    """
    formatted_chunks = []
    try:
        pages = convert_from_path(path)
        for page_num, pil_img in enumerate(pages):
            ocr_data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
            n_boxes = len(ocr_data['text'])
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                if len(text) < MIN_TEXT_LENGTH:
                    continue
                fmt = {
                    "text": text,
                    "font_size_approx": ocr_data['height'][i],  # bbox height as approx font size
                    "left": ocr_data['left'][i],
                    "top": ocr_data['top'][i],
                    "width": ocr_data['width'][i],
                    "height": ocr_data['height'][i],
                    "page_num": page_num,
                    "note": "Approximate formatting from OCR bounding box"
                }
                # Future: approximate alignment could be inferred here using left/x0 values if needed
                formatted_chunks.append(fmt)
    except Exception as e:
        logger.error(f"[extract_formatting_scanned_pdf] Error: {e}")
    return formatted_chunks


def extract_formatting_image(path: str) -> List[Dict[str, Any]]:
    """
    Extract formatting info from an image file (PNG, JPG, etc.)
    using OCR bounding boxes as approximate formatting.
    Filters out short/empty text.
    """
    formatted_chunks = []
    try:
        pil_img = Image.open(path)
        ocr_data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            text = ocr_data['text'][i].strip()
            if len(text) < MIN_TEXT_LENGTH:
                continue
            fmt = {
                "text": text,
                "font_size_approx": ocr_data['height'][i],
                "left": ocr_data['left'][i],
                "top": ocr_data['top'][i],
                "width": ocr_data['width'][i],
                "height": ocr_data['height'][i],
                "note": "Approximate formatting from OCR bounding box"
            }
            formatted_chunks.append(fmt)
    except Exception as e:
        logger.error(f"[extract_formatting_image] Error: {e}")
    return formatted_chunks


def extract_formatting(path: str) -> List[Dict[str, Any]]:
    """
    Master function to decide extraction method based on file extension.
    For PDFs, tries native extraction first, then OCR fallback if native text is insufficient.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return extract_formatting_docx(path)

    if ext == ".pdf":
        # Try native PDF extraction
        native_fmt = extract_formatting_pdf(path)
        # If native extraction finds too little text, fallback to OCR
        if len(native_fmt) < 10:
            logger.info(f"Native PDF extraction found {len(native_fmt)} text chunks, falling back to OCR.")
            return extract_formatting_scanned_pdf(path)
        return native_fmt

    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return extract_formatting_image(path)

    logger.warning(f"[extract_formatting] Unsupported file extension: {ext}")
    return []


def compare_formatting(doc1_fmt: List[Dict[str, Any]], doc2_fmt: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Compare two formatting lists.

    Returns a dict with keys:
      - "added": formatting chunks in doc2 but not in doc1
      - "removed": formatting chunks in doc1 but not in doc2
      - "changed": same text in both but with different formatting attributes

    Comparison uses text as primary key, ignoring metadata fields.
    """
    added, removed, changed = [], [], []

    def fmt_key(fmt: Dict[str, Any]) -> str:
        # Use normalized text as key for comparison
        return fmt.get("text", "").strip()

    idx1 = {fmt_key(item): item for item in doc1_fmt if fmt_key(item)}
    idx2 = {fmt_key(item): item for item in doc2_fmt if fmt_key(item)}

    # Check added or changed
    for text, fmt2 in idx2.items():
        fmt1 = idx1.get(text)
        if not fmt1:
            added.append(fmt2)
        else:
            # Compare all keys except text, page_num, note (non-formatting metadata)
            keys_to_compare = set(fmt1.keys()).intersection(fmt2.keys()) - {"text", "page_num", "note"}
            diffs = {}
            for k in keys_to_compare:
                if fmt1.get(k) != fmt2.get(k):
                    diffs[k] = {"doc1": fmt1.get(k), "doc2": fmt2.get(k)}
            if diffs:
                changed.append({"text": text, "differences": diffs})

    # Check removed
    for text, fmt1 in idx1.items():
        if text not in idx2:
            removed.append(fmt1)

    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
