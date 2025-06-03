from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Tuple
import os
import uuid
import shutil
from pathlib import Path

from app.config import settings
from app.models.schemas import UploadResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.jpg', '.jpeg', '.png'}

def save_file(file: UploadFile, upload_dir: Path) -> Tuple[str, str]:
    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    
    # Create secure filename
    file_id = str(uuid.uuid4())
    save_path = upload_dir / f"{file_id}{ext}"
    
    # Save the file
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_id, str(save_path)

@router.post("/upload/", response_model=UploadResponse)
async def upload_documents(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    Accepts two document files and saves them securely.
    """
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    try:
        file1_id, file1_path = save_file(file1, upload_dir)
        file2_id, file2_path = save_file(file2, upload_dir)

        return UploadResponse(
            message="Files uploaded successfully.",
            file1_id=file1_id,
            file2_id=file2_id,
            file1_path=file1_path,
            file2_path=file2_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
