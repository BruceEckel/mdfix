"""Configuration settings for md-semlinebreak."""

from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    """Configuration options for markdown formatting."""
    
    # Line length settings
    max_line_length: int = 80
    soft_wrap_length: int = 70
    
    # Breaking behavior
    break_at_conjunctions: bool = True
    break_at_clauses: bool = True
    break_at_sentences: bool = True
    
    # Punctuation that triggers clause breaks
    clause_break_punctuation: List[str] = None
    
    # Conjunctions that can trigger breaks (only after punctuation)
    conjunction_words: List[str] = None
    
    # Unicode normalization
    normalize_unicode: bool = False
    
    def __post_init__(self):
        """Set default values for mutable fields."""
        if self.clause_break_punctuation is None:
            self.clause_break_punctuation = [',', ':', ';']
            
        if self.conjunction_words is None:
            self.conjunction_words = ['and', 'but', 'or', 'yet', 'so', 'for', 'nor']


# Default configuration instance
DEFAULT_CONFIG = Config()