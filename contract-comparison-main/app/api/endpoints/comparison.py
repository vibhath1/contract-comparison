from fastapi import APIRouter, HTTPException, Query
from app.core.document_processor import extract_text
from app.core.comparison_engine import compare_documents
import os

router = APIRouter()

@router.get("/compare/")
def compare_documents_api(file1: str = Query(...), file2: str = Query(...)):
    """
    Compare two documents by file paths.
    Example: /compare/?file1=uploads/a.pdf&file2=uploads/b.docx
    """
    if not os.path.exists(file1):
        raise HTTPException(status_code=404, detail=f"File not found: {file1}")
    if not os.path.exists(file2):
        raise HTTPException(status_code=404, detail=f"File not found: {file2}")

    try:
        text1 = extract_text(file1)
        text2 = extract_text(file2)
        result = compare_documents(text1, text2, file1, file2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
