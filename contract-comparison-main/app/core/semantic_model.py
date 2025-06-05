# app/core/semantic_model.py

try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False
    print("Warning: sentence-transformers not available.")

_model = None

def get_semantic_model(model_name: str = "paraphrase-MiniLM-L6-v2"):
    global _model
    if not MODEL_AVAILABLE:
        return None
    if _model is None:
        _model = SentenceTransformer(model_name)
        print(f"Loaded semantic similarity model: {model_name}")
    return _model
