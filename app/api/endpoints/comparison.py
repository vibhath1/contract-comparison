from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
from app.models.schemas import (
    ComparisonRequest, ComparisonResult, ComparisonStatus,
    Difference, DifferenceType
)
from app.core.document_processor import DocumentProcessor
from app.core.comparison_engine import ComparisonEngine
from app.core.ai_analyzer import AIAnalyzer
from app.config import settings
import uuid
from pathlib import Path
import os
import json
import asyncio

router = APIRouter()

# In-memory storage for statuses (replace with database in production)
comparison_statuses = {}

document_processor = DocumentProcessor(settings.UPLOAD_DIR)
comparison_engine = ComparisonEngine()
ai_analyzer = AIAnalyzer(settings.SEMANTIC_MODEL)

async def process_comparison(
    comparison_id: uuid.UUID,
    original_doc_id: uuid.UUID,
    modified_doc_id: uuid.UUID
):
    try:
        # Update status to processing
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="processing",
            progress=0.1,
            message="Starting document processing"
        )
        
        # Find document files
        original_file = None
        modified_file = None
        
        for filename in os.listdir(settings.UPLOAD_DIR):
            file_id_str = os.path.splitext(filename)[0]
            try:
                file_id = uuid.UUID(file_id_str)
                if file_id == original_doc_id:
                    original_file = settings.UPLOAD_DIR / filename
                elif file_id == modified_doc_id:
                    modified_file = settings.UPLOAD_DIR / filename
            except ValueError:
                continue
        
        if not original_file or not modified_file:
            comparison_statuses[comparison_id] = ComparisonStatus(
                comparison_id=comparison_id,
                status="failed",
                message="One or both documents not found"
            )
            return
            
        # Update status
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="processing",
            progress=0.2,
            message="Processing original document"
        )
        
        # Process documents
        original_content = document_processor.process_document(original_file)
        
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="processing",
            progress=0.4,
            message="Processing modified document"
        )
        
        modified_content = document_processor.process_document(modified_file)
        
        # Update status
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="processing",
            progress=0.6,
            message="Comparing documents"
        )
        
        # Compare documents
        differences = comparison_engine.compare_texts(
            original_content["text"], 
            modified_content["text"]
        )
        
        # Update status
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="processing",
            progress=0.8,
            message="Analyzing differences with AI"
        )
        
        # Enhance with AI analysis
        enhanced_differences = ai_analyzer.analyze_differences(differences)
        
        # Generate summary
        summary = ai_analyzer.generate_summary(enhanced_differences)
        
        # Calculate similarity score
        similarity_score = comparison_engine.compute_similarity_score(
            original_content["text"],
            modified_content["text"]
        )
        
        # Create result
        result = ComparisonResult(
            comparison_id=comparison_id,
            original_document_id=original_doc_id,
            modified_document_id=modified_doc_id,
            differences=enhanced_differences,
            summary=summary,
            similarity_score=similarity_score
        )
        
        # Save result
        result_path = settings.RESULT_DIR / f"{comparison_id}.json"
        with open(result_path, "w") as f:
            # Convert to dict for JSON serialization
            f.write(result.json())
        
        # Update status to completed
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="completed",
            progress=1.0,
            message="Comparison completed successfully"
        )
        
    except Exception as e:
        # Update status to failed
        comparison_statuses[comparison_id] = ComparisonStatus(
            comparison_id=comparison_id,
            status="failed",
            message=f"Error during comparison: {str(e)}"
        )

@router.post("/", response_model=ComparisonStatus)
async def create_comparison(
    request: ComparisonRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new comparison between two documents.
    """
    comparison_id = uuid.uuid4()
    
    # Initialize status
    status = ComparisonStatus(
        comparison_id=comparison_id,
        status="queued",
        progress=0.0,
        message="Comparison queued"
    )
    comparison_statuses[comparison_id] = status
    
    # Start processing in the background
    background_tasks.add_task(
        process_comparison,
        comparison_id,
        request.original_document_id,
        request.modified_document_id
    )
    
    return status

@router.get("/status/{comparison_id}", response_model=ComparisonStatus)
async def get_comparison_status(comparison_id: uuid.UUID):
    """
    Get the status of a comparison.
    """
    if comparison_id not in comparison_statuses:
        raise HTTPException(
            status_code=404,
            detail=f"Comparison with ID {comparison_id} not found"
        )
    
    return comparison_statuses[comparison_id]

@router.get("/result/{comparison_id}", response_model=ComparisonResult)
async def get_comparison_result(comparison_id: uuid.UUID):
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
    
    # Load result from file
    result_path = settings.RESULT_DIR / f"{comparison_id}.json"
    if not os.path.exists(result_path):
        raise HTTPException(
            status_code=404,
            detail=f"Result file not found for comparison ID {comparison_id}"
        )
        
    try:
        with open(result_path, "r") as f:
            result_data = json.load(f)
            return ComparisonResult(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading comparison result: {str(e)}"
        )