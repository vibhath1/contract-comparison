# Update main.py to remove duplicate directory creation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.endpoints import upload, comparison
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(upload.router, prefix=settings.API_V1_STR + "/documents", tags=["documents"])
app.include_router(comparison.router, prefix=settings.API_V1_STR + "/comparison", tags=["comparison"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Contract Comparison AI API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
