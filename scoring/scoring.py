"""
THIS FILE IS DEPRECATED

Scorer and BestOfNBuilder have been moved to their respective modules:
- Scorer: scoring.scorer
- BestOfNBuilder: scoring.best_of_n

This file exists for backward compatibility.
"""

import warnings
from scoring.scorer import Scorer
from scoring.best_of_n import BestOfNBuilder

# Show deprecation warning
warnings.warn(
    "Importing from scoring.scoring is deprecated. "
    "Import Scorer from scoring.scorer and BestOfNBuilder from scoring.best_of_n instead.",
    DeprecationWarning, stacklevel=2
)

__all__ = ["Scorer", "BestOfNBuilder"] 