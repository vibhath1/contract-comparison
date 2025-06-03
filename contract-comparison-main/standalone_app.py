# Update standalone_app.py to use explicit paths
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
import os
import uuid
from datetime import datetime
import shutil
from pathlib import Path

# Get the absolute path to the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploads")
RESULT_DIR = os.path.join(CURRENT_DIR, "results")

# Print paths for debugging
print(f"Current directory: {CURRENT_DIR}")
print(f"Upload directory: {UPLOAD_DIR}")
print(f"Result directory: {RESULT_DIR}")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# Create app
app = FastAPI(title="Contract Comparison API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    TEXT = "text"

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    document_type: Optional[DocumentType] = None
    upload_time: datetime = Field(default_factory=datetime.now)
    status: str = "uploaded"

class ComparisonRequest(BaseModel):
    original_document_id: str
    modified_document_id: str
    comparison_level: str = "detailed"  # basic, detailed, ai-enhanced

class DifferenceType(str, Enum):
    ADDITION = "addition"
    DELETION = "deletion"
    MODIFICATION = "modification"
    FORMAT_CHANGE = "format_change"
    VISUAL_CHANGE = "visual_change"

class Difference(BaseModel):
    type: DifferenceType
    location: Dict[str, Any]  # Flexible structure to identify location in document
    original_content: Optional[str] = None
    modified_content: Optional[str] = None
    importance: Optional[str] = None  # low, medium, high
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class ComparisonResult(BaseModel):
    comparison_id: str
    original_document_id: str
    modified_document_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    differences: List[Difference] = []
    summary: Optional[str] = None
    similarity_score: Optional[float] = None

class ComparisonStatus(BaseModel):
    comparison_id: str
    status: str  # "queued", "processing", "completed", "failed"
    progress: Optional[float] = None
    message: Optional[str] = None

# In-memory storage for statuses (replace with database in production)
comparison_statuses = {}

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Contract Comparison AI API"}

@app.post("/api/v1/documents/upload/", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for comparison.
    """
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    # Validate file format
    valid_extensions = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.txt']
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_extension}. Supported formats are: {', '.join(valid_extensions)}"
        )
    
    # Determine document type
    document_type = None
    if file_extension == '.pdf':
        document_type = DocumentType.PDF
    elif file_extension in ['.docx', '.doc']:
        document_type = DocumentType.DOCX
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        document_type = DocumentType.IMAGE
    elif file_extension == '.txt':
        document_type = DocumentType.TEXT
    
    # Create file path with explicit path
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
    
    print(f"Saving file to: {file_path}")
    
    # Save file
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )
    
    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        document_type=document_type,
        status="uploaded"
    )

@app.get("/api/v1/documents/", response_model=List[UploadResponse])
async def list_documents():
    """
    List all uploaded documents.
    """
    # This is a simplified implementation that reads from the upload directory
    
    documents = []
    for filename in os.listdir(UPLOAD_DIR):
        try:
            file_path = os.path.join(UPLOAD_DIR, filename)
            file_id_with_ext = os.path.basename(filename)
            file_id_str = os.path.splitext(file_id_with_ext)[0]
            file_ext = os.path.splitext(file_id_with_ext)[1].lower()
            
            # Determine document type from extension
            document_type = None
            if file_ext == '.pdf':
                document_type = DocumentType.PDF
            elif file_ext in ['.docx', '.doc']:
                document_type = DocumentType.DOCX
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                document_type = DocumentType.IMAGE
            elif file_ext == '.txt':
                document_type = DocumentType.TEXT
            else:
                continue  # Skip unknown file types
                
            documents.append(
                UploadResponse(
                    file_id=file_id_str,
                    filename=file_id_with_ext,  # Using the stored filename as we don't have the original
                    document_type=document_type,
                    status="uploaded"
                )
            )
        except Exception as e:
            # Skip files that cause errors
            continue
            
    return documents

@app.post("/api/v1/comparison/", response_model=ComparisonStatus)
async def create_comparison(
    request: ComparisonRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new comparison between two documents.
    """
    comparison_id = str(uuid.uuid4())
    
    # Initialize status
    status = ComparisonStatus(
        comparison_id=comparison_id,
        status="queued",
        progress=0.0,
        message="Comparison queued for processing"
    )
    comparison_statuses[comparison_id] = status
    
    # In a real implementation, we would start processing in the background
    # For now, just simulate completion
    
    # Update status after a delay
    background_tasks.add_task(
        simulate_processing,
        comparison_id,
        request.original_document_id,
        request.modified_document_id
    )
    
    return status

async def simulate_processing(comparison_id, original_doc_id, modified_doc_id):
    """Simulate processing a comparison."""
    import asyncio
    
    # Update status to processing
    comparison_statuses[comparison_id] = ComparisonStatus(
        comparison_id=comparison_id,
        status="processing",
        progress=0.2,
        message="Processing documents"
    )
    
    # Simulate some processing time
    await asyncio.sleep(2)
    
    # Update progress
    comparison_statuses[comparison_id] = ComparisonStatus(
        comparison_id=comparison_id,
        status="processing",
        progress=0.6,
        message="Comparing documents"
    )
    
    # Simulate more processing time
    await asyncio.sleep(2)
    
    # Update status to completed
    comparison_statuses[comparison_id] = ComparisonStatus(
        comparison_id=comparison_id,
        status="completed",
        progress=1.0,
        message="Comparison completed successfully"
    )
    
    # Save a mock result
    result = ComparisonResult(
        comparison_id=comparison_id,
        original_document_id=original_doc_id,
        modified_document_id=modified_doc_id,
        differences=[
            Difference(
                type=DifferenceType.ADDITION,
                location={"line": 10},
                modified_content="This is a sample addition",
                importance="medium",
                confidence=0.9
            ),
            Difference(
                type=DifferenceType.DELETION,
                location={"line": 15},
                original_content="This content was deleted",
                importance="high",
                confidence=0.95
            )
        ],
        summary="Found 2 differences: 1 addition and 1 deletion",
        similarity_score=0.85
    )
    
    # In a real implementation, we'd save this to a file or database
    # For now, just keep it in memory
    
@app.get("/api/v1/comparison/status/{comparison_id}", response_model=ComparisonStatus)
async def get_comparison_status(comparison_id: str):
    """
    Get the status of a comparison.
    """
    if comparison_id not in comparison_statuses:
        raise HTTPException(
            status_code=404,
            detail=f"Comparison with ID {comparison_id} not found"
        )
    
    return comparison_statuses[comparison_id]

@app.get("/api/v1/comparison/result/{comparison_id}", response_model=ComparisonResult)
async def get_comparison_result(comparison_id: str):
    """
    Get the result of a completed comparison.
    """
    # Check if the comparison exists and is completed
    if comparison_id not in comparison_statuses:
        raise HTTPException(
            status_code=404,
            detail=f"Comparison with ID {comparison_id} not found"
        )
        
    status = comparison_statuses[comparison_id]
    if status.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Comparison is not completed yet. Current status: {status.status}"
        )
    
    # In a real implementation, we'd load this from a file or database
    # For now, just create a mock result
    
    return ComparisonResult(
        comparison_id=comparison_id,
        original_document_id="original-doc-id",  # This would be the actual ID in a real implementation
        modified_document_id="modified-doc-id",  # This would be the actual ID in a real implementation
        differences=[
            Difference(
                type=DifferenceType.ADDITION,
                location={"line": 10},
                modified_content="This is a sample addition",
                importance="medium",
                confidence=0.9
            ),
            Difference(
                type=DifferenceType.DELETION,
                location={"line": 15},
                original_content="This content was deleted",
                importance="high",
                confidence=0.95
            )
        ],
        summary="Found 2 differences: 1 addition and 1 deletion",
        similarity_score=0.85
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("standalone_app:app", host="0.0.0.0", port=8000, reload=True)
