# Update upload.py with more robust file handling
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import uuid
import os
from pathlib import Path
import shutil
from app.config import settings
from app.models.schemas import UploadResponse, DocumentType

router = APIRouter()

@router.post("/upload/", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for comparison.
    """
    try:
        # Print debugging information
        print(f"Upload directory: {settings.UPLOAD_DIR}")
        print(f"Upload directory exists: {os.path.exists(str(settings.UPLOAD_DIR))}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Generate unique file ID
        file_id = uuid.uuid4()
        
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
        
        # Create upload directory if it doesn't exist (double-check)
        upload_dir_str = str(settings.UPLOAD_DIR)
        os.makedirs(upload_dir_str, exist_ok=True)
        
        # List files in the upload directory
        try:
            print("Files in upload directory:")
            for existing_file in os.listdir(upload_dir_str):
                print(f"  - {existing_file}")
        except Exception as e:
            print(f"Error listing directory: {e}")
        
        # Create file path
        file_path = os.path.join(upload_dir_str, f"{file_id}{file_extension}")
        
        print(f"Saving file to: {file_path}")
        
        # Try creating a test file first to verify directory write permissions
        test_file_path = os.path.join(upload_dir_str, "test_upload.txt")
        try:
            with open(test_file_path, "w") as test_file:
                test_file.write("Test file for upload verification")
            print(f"Successfully created test file: {test_file_path}")
            os.remove(test_file_path)  # Clean up the test file
            print("Test file removed")
        except Exception as e:
            print(f"Error creating test file: {e}")
            # Try alternative upload directory
            alternative_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(alternative_dir, exist_ok=True)
            file_path = os.path.join(alternative_dir, f"{file_id}{file_extension}")
            print(f"Trying alternative location: {file_path}")
        
        # Save file
        try:
            # Read the file content
            file_content = await file.read()
            
            # Write to file using direct write
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            print(f"File saved successfully to: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            print(f"File size: {os.path.getsize(file_path)} bytes")
        except Exception as e:
            print(f"Error saving file with direct write: {str(e)}")
            
            # Try alternative approach
            try:
                # Create a temporary file
                temp_file_path = os.path.join(os.getcwd(), f"temp_{file_id}{file_extension}")
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(file_content)
                
                print(f"Temporary file created at: {temp_file_path}")
                
                # Copy to final location
                shutil.copy2(temp_file_path, file_path)
                os.remove(temp_file_path)  # Clean up
                
                print(f"File copied to final location: {file_path}")
                print(f"File exists: {os.path.exists(file_path)}")
            except Exception as e2:
                print(f"Error with alternative approach: {str(e2)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error saving file: {str(e)} / Alternative error: {str(e2)}"
                )
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            document_type=document_type,
            status="uploaded"
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Exception in upload_document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing upload: {str(e)}"
        )

@router.get("/", response_model=List[UploadResponse])
async def list_documents():
    """
    List all uploaded documents.
    """
    try:
        # This is a simplified implementation that reads from the upload directory
        # In a production system, this would typically read from a database
        
        documents = []
        upload_dir_str = str(settings.UPLOAD_DIR)
        
        print(f"Listing documents from: {upload_dir_str}")
        print(f"Directory exists: {os.path.exists(upload_dir_str)}")
        
        try:
            for filename in os.listdir(upload_dir_str):
                try:
                    file_path = os.path.join(upload_dir_str, filename)
                    file_id_with_ext = os.path.basename(filename)
                    file_id_str = os.path.splitext(file_id_with_ext)[0]
                    file_ext = os.path.splitext(file_id_with_ext)[1].lower()
                    
                    try:
                        file_id = uuid.UUID(file_id_str)
                    except ValueError:
                        # Skip files with invalid UUIDs
                        continue
                        
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
                            file_id=file_id,
                            filename=file_id_with_ext,  # Using the stored filename as we don't have the original
                            document_type=document_type,
                            status="uploaded"
                        )
                    )
                except Exception as e:
                    # Skip files that cause errors
                    print(f"Error processing file {filename}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error listing directory: {str(e)}")
            
        return documents
    except Exception as e:
        print(f"Exception in list_documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )
