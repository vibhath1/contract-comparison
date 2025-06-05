from pydantic_settings import BaseSettings
from pathlib import Path
import os

BASE_DIR: Path = Path(__file__).resolve().parent.parent  # app/config.py

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Contract Comparison API"
    
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    RESULT_DIR: Path = BASE_DIR / "results"
    
    USE_GPU: bool = False
    SEMANTIC_MODEL: str = "paraphrase-MiniLM-L6-v2"

    class Config:
        case_sensitive = True
        env_file = ".env"  # optional for .env support

settings = Settings()

def ensure_directories():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.RESULT_DIR, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    if os.getenv("DEBUG_CONFIG", "false").lower() == "true":
        print(f"UPLOAD_DIR: {settings.UPLOAD_DIR}")
        print(f"RESULT_DIR: {settings.RESULT_DIR}")
