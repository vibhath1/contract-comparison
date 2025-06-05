from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

try:
    from app.api.endpoints import comparison
    from app.config import settings, ensure_directories
except ImportError as e:
    raise ImportError(
        f"Failed to import required modules. "
        f"Make sure your project structure is correct and PYTHONPATH includes the project root. "
        f"Original error: {e}"
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    Creates required directories on startup.
    """
    # Ensure directories exist on startup
    ensure_directories()
    yield
    # Add shutdown logic here if needed in future

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Configure CORS middleware with wide-open policy (adjust for production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Normalize API prefix path to avoid double slashes
api_prefix = settings.API_V1_STR.rstrip("/")

# Include only the comparison router under /api/v1/comparison (or whatever prefix you use)
app.include_router(
    comparison.router,
    prefix=f"{api_prefix}/comparison",
    tags=["comparison"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Contract Comparison AI API"}

if __name__ == "__main__":
    # Run with reload in dev; remove reload for production
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
