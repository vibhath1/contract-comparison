# Update config.py with corrected path resolution
from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Get the correct base directory of the project
# __file__ is in app/config.py, so we need to go up two levels to reach the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Alternative approach - hardcode the path to be certain
PROJECT_ROOT = Path('C:/Users/ASUS/Documents/GitHub/contract-comparison')

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Contract Comparison API"
    
    # Storage paths with absolute paths - using the hardcoded path for reliability
    UPLOAD_DIR: Path = PROJECT_ROOT / "uploads"
    RESULT_DIR: Path = PROJECT_ROOT / "results"
    
    # AI model settings
    USE_GPU: bool = False
    SEMANTIC_MODEL: str = "paraphrase-MiniLM-L6-v2"
    
    class Config:
        case_sensitive = True

settings = Settings()

# Print paths for debugging
print(f"BASE_DIR (from __file__): {BASE_DIR}")
print(f"PROJECT_ROOT (hardcoded): {PROJECT_ROOT}")
print(f"Upload directory: {settings.UPLOAD_DIR}")
print(f"Result directory: {settings.RESULT_DIR}")

# Create directories if they don't exist
os.makedirs(str(settings.UPLOAD_DIR), exist_ok=True)
os.makedirs(str(settings.RESULT_DIR), exist_ok=True)

# Verify directories were created
print(f"Upload directory exists: {os.path.exists(str(settings.UPLOAD_DIR))}")
print(f"Result directory exists: {os.path.exists(str(settings.RESULT_DIR))}")
