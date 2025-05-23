from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    TEXT = "text"

class UploadResponse(BaseModel):
    file_id: UUID = Field(default_factory=uuid4)
    filename: str
    document_type: DocumentType
    upload_time: datetime = Field(default_factory=datetime.now)
    status: str = "uploaded"

class ComparisonRequest(BaseModel):
    original_document_id: UUID
    modified_document_id: UUID
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
    comparison_id: UUID = Field(default_factory=uuid4)
    original_document_id: UUID
    modified_document_id: UUID
    timestamp: datetime = Field(default_factory=datetime.now)
    differences: List[Difference] = []
    summary: Optional[str] = None
    similarity_score: Optional[float] = None
    
class ComparisonStatus(BaseModel):
    comparison_id: UUID
    status: str  # "queued", "processing", "completed", "failed"
    progress: Optional[float] = None
    message: Optional[str] = None