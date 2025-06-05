#ai_analyzer.py
from app.core.semantic_model import get_semantic_model
from typing import Dict, List, Any, Optional
import numpy as np
from app.models.schemas import Difference

try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Using fallback similarity measures.")
    MODEL_AVAILABLE = False

class AIAnalyzer:
    def __init__(self, model_name: str = "paraphrase-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = get_semantic_model(model_name)
        
        
    def analyze_differences(self, differences: List[Difference]) -> List[Difference]:
        enhanced_differences = []
        for diff in differences:
            enhanced_diff = diff.dict()
            orig = diff.original_content or ""
            mod = diff.modified_content or ""

            if orig and mod:
                similarity = self._compute_semantic_similarity(orig, mod)
                importance = self._analyze_importance(orig, mod, similarity)
                enhanced_diff["confidence"] = round(1.0 - similarity, 4)
                enhanced_diff["importance"] = importance

            enhanced_differences.append(Difference(**enhanced_diff))
        return enhanced_differences

    def _analyze_importance(self, original: str, modified: str, similarity: float) -> str:
        important_terms = [
            "shall", "must", "will not", "required", "payment", "terminate",
            "warranty", "liability", "damages", "agree", "obligation"
        ]

        original_has = any(term in original.lower() for term in important_terms)
        modified_has = any(term in modified.lower() for term in important_terms)
        if original_has != modified_has:
            return "high"

        if similarity < 0.6:
            return "high"
        elif similarity < 0.85:
            return "medium"
        return "low"

    def _compute_semantic_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0

        if self.model is not None:
            try:
                emb = self.model.encode([text1, text2], convert_to_numpy=True)
                emb1, emb2 = emb[0], emb[1]
                return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
            except Exception as e:
                print(f"Error computing similarity: {e}")

        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0

    def generate_summary(self, differences: List[Difference]) -> Dict[str, Any]:
        additions = sum(1 for d in differences if d.type == "addition")
        deletions = sum(1 for d in differences if d.type == "deletion")
        modifications = sum(1 for d in differences if d.type == "modification")

        high = sum(1 for d in differences if d.importance == "high")
        medium = sum(1 for d in differences if d.importance == "medium")
        low = sum(1 for d in differences if d.importance == "low")

        summary_text = (
            f"Found {len(differences)} differences: {additions} additions, {deletions} deletions, and {modifications} modifications. "
        )
        if high or medium or low:
            summary_text += (
                f"{high} high importance, {medium} medium importance, and {low} low importance changes."
            )

        return {
            "text": summary_text,
            "counts": {
                "total": len(differences),
                "additions": additions,
                "deletions": deletions,
                "modifications": modifications,
                "high": high,
                "medium": medium,
                "low": low
            }
        }

    def compare_pair(self, original: str, modified: str) -> Dict[str, Any]:
        similarity = self._compute_semantic_similarity(original, modified)
        importance = self._analyze_importance(original, modified, similarity)
        return {
            "importance": importance,
            "confidence": round(1.0 - similarity, 4)
        }
