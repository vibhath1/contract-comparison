import difflib
from typing import List, Dict, Any
import re
from app.models.schemas import Difference, DifferenceType

class ComparisonEngine:
    def __init__(self):
        pass
    
    def compare_texts(self, original_text: str, modified_text: str) -> List[Difference]:
        """Compare two texts and identify differences."""
        # Split texts into lines
        original_lines = original_text.splitlines()
        modified_lines = modified_text.splitlines()
        
        # Get diff
        differ = difflib.Differ()
        diff = list(differ.compare(original_lines, modified_lines))
        
        # Process differences
        differences = []
        for i, line in enumerate(diff):
            if line.startswith('+ '):  # Addition
                differences.append(Difference(
                    type=DifferenceType.ADDITION,
                    location={"line_approx": i},
                    modified_content=line[2:],
                    importance="medium"
                ))
            elif line.startswith('- '):  # Deletion
                differences.append(Difference(
                    type=DifferenceType.DELETION,
                    location={"line_approx": i},
                    original_content=line[2:],
                    importance="medium"
                ))
            elif line.startswith('? '):  # Details about changes
                continue
            
        # Compare paragraphs for more detailed analysis
        paragraph_differences = self._compare_paragraphs(original_text, modified_text)
        differences.extend(paragraph_differences)
        
        return differences
    
    def _compare_paragraphs(self, original_text: str, modified_text: str) -> List[Difference]:
        """Compare text at paragraph level to detect modifications."""
        # Split by double newlines (paragraphs)
        original_paragraphs = re.split(r'\n\s*\n', original_text)
        modified_paragraphs = re.split(r'\n\s*\n', modified_text)
        
        # Compare paragraphs
        matcher = difflib.SequenceMatcher(None, original_paragraphs, modified_paragraphs)
        differences = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                # This is a modification - paragraphs were changed
                for i in range(i1, i2):
                    for j in range(j1, j2):
                        # Simplified approach - in real implementation we'd want to 
                        # do more detailed comparison within paragraphs
                        differences.append(Difference(
                            type=DifferenceType.MODIFICATION,
                            location={"paragraph": i},
                            original_content=original_paragraphs[i],
                            modified_content=modified_paragraphs[j],
                            importance="high"
                        ))
                        
        return differences
    
    def compute_similarity_score(self, original_text: str, modified_text: str) -> float:
        """Compute a simple similarity score between documents."""
        seq_matcher = difflib.SequenceMatcher(None, original_text, modified_text)
        return seq_matcher.ratio()