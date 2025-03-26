"""
Hephaestus Engine Module

This module contains the components responsible for the core functionality
of the Hephaestus system, including code generation, mutation, and loop control.
"""

import warnings
import sys
import os
from pathlib import Path

# Add parent directory to path to ensure imports work
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Forward compatibility imports
try:
    from scoring.best_of_n import BestOfNBuilder as NewBestOfNBuilder

    class BestOfNBuilder(NewBestOfNBuilder):
        """Compatibility wrapper for BestOfNBuilder."""
        
        def __init__(self, *args, **kwargs):
            warnings.warn(
                "Importing BestOfNBuilder from engine is deprecated. Import from scoring.best_of_n instead.",
                DeprecationWarning, stacklevel=2
            )
            super().__init__(*args, **kwargs)
except ImportError:
    # If the new implementation isn't available yet, fall back to the original
    from engine.best_of_n import BestOfNBuilder
    warnings.warn(
        "Using legacy BestOfNBuilder implementation. This will be removed in a future version.",
        DeprecationWarning, stacklevel=2
    )

# Define module exports
__all__ = [
    'BestOfNBuilder',
    'ForgeLoop',
    'MutationEngine',
    'FlowBuilderNode',
] 