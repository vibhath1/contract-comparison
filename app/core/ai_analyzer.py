from typing import Dict, List, Any
import numpy as np
from app.models.schemas import Difference

# Try to import sentence-transformers, but provide fallbacks if not available
try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Using fallback similarity measures.")
    MODEL_AVAILABLE = False

class AIAnalyzer:
    def __init__(self, model_name: str = "paraphrase-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        
        # Initialize model if available
        if MODEL_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                print(f"Loaded semantic similarity model: {model_name}")
            except Exception as e:
                print(f"Error loading model: {str(e)}")
    
    def analyze_differences(self, differences: List[Difference]) -> List[Difference]:
        """Enhance differences with AI analysis."""
        # This is a placeholder implementation
        # In a real implementation, we'd analyze the differences more thoroughly
        
        enhanced_differences = []
        for diff in differences:
            # Create a copy of the difference to modify
            enhanced_diff = diff.dict()
            
            # Analyze importance based on content if available
            if diff.original_content and diff.modified_content:
                importance = self._analyze_importance(diff.original_content, diff.modified_content)
                enhanced_diff["importance"] = importance
                
                # Add confidence based on semantic similarity
                similarity = self._compute_semantic_similarity(diff.original_content, diff.modified_content)
                enhanced_diff["confidence"] = 1.0 - similarity  # Higher difference = higher confidence
            
            # Add the enhanced difference to the list
            enhanced_differences.append(Difference(**enhanced_diff))
            
        return enhanced_differences
    
    def _analyze_importance(self, original: str, modified: str) -> str:
        """Analyze the importance of a change."""
        # This is a simplified implementation
        # In reality, we'd use more sophisticated NLP techniques
        
        # Look for key terms that might indicate important changes
        important_terms = [
            "shall", "must", "will not", "required", "payment", "terminate",
            "warranty", "liability", "damages", "agree", "obligation"
        ]
        
        # Check if any important terms were added or removed
        original_has_terms = any(term in original.lower() for term in important_terms)
        modified_has_terms = any(term in modified.lower() for term in important_terms)
        
        if original_has_terms != modified_has_terms:
            return "high"
        
        # Length-based heuristic
        if len(original) > 100 or len(modified) > 100:
            return "medium"
            
        return "low"
    
    def _compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts."""
        if not text1 or not text2:
            return 0.0
            
        # If model is available, use it for semantic similarity
        if self.model is not None:
            try:
                # Encode the texts
                embedding1 = self.model.encode(text1, convert_to_numpy=True)
                embedding2 = self.model.encode(text2, convert_to_numpy=True)
                
                # Compute cosine similarity
                similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
                return float(similarity)
            except Exception as e:
                print(f"Error computing semantic similarity: {str(e)}")
                # Fall back to basic similarity
        
        # Fallback to basic similarity measure
        # Calculate Jaccard similarity between words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
            
        return intersection / union
    
    def generate_summary(self, differences: List[Difference]) -> str:
        """Generate a summary of the differences."""
        # Count types of differences
        additions = sum(1 for diff in differences if diff.type == "addition")
        deletions = sum(1 for diff in differences if diff.type == "deletion")
        modifications = sum(1 for diff in differences if diff.type == "modification")
        
        # Count by importance
        high_importance = sum(1 for diff in differences if diff.importance == "high")
        medium_importance = sum(1 for diff in differences if diff.importance == "medium")
        low_importance = sum(1 for diff in differences if diff.importance == "low")
        
        # Generate summary
        summary = f"Found {len(differences)} differences: {additions} additions, {deletions} deletions, and {modifications} modifications. "
        
        if high_importance > 0:
            summary += f"{high_importance} changes were identified as high importance, "
            summary += f"{medium_importance} as medium importance, and {low_importance} as low importance."
        
        return summary