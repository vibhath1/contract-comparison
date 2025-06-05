from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.comparison_engine import compare_documents
import tempfile
import shutil
import os

router = APIRouter()

@router.post("/compare/")
async def compare_documents_endpoint(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Save uploaded files to temp files to support all file types (PDF, DOCX, images, etc.)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file1.filename)[1]) as tmp1:
            shutil.copyfileobj(file1.file, tmp1)
            path1 = tmp1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file2.filename)[1]) as tmp2:
            shutil.copyfileobj(file2.file, tmp2)
            path2 = tmp2.name
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving uploaded files: {str(e)}")

    try:
        # Dynamically build the YOLO model path relative to this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))  # app/api/endpoints
        app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))  # app
        yolo_model_path = os.path.join(app_dir, "models", "signatureyolo.pt")

        # Call the compare_documents function with file paths and filenames
        result = compare_documents(path1, path2, file1.filename, file2.filename, yolo_model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing documents: {str(e)}")
    finally:
        # Clean up temporary files after processing
        try:
            os.remove(path1)
            os.remove(path2)
        except Exception:
            pass

    return result
