"""
Flow module - DEPRECATED

This module has been moved to core.flow
Importing from nodes.flow is deprecated and will be removed in a future version.
"""

import warnings
import sys
from pathlib import Path

# Add parent directory to path to ensure imports work
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Import from the new location
from core.flow import Flow, BatchNode, BatchFlow

# Show deprecation warning
warnings.warn(
    "Importing from nodes.flow is deprecated. Use 'from core.flow import Flow, BatchNode, BatchFlow' instead.",
    DeprecationWarning, stacklevel=2
)

# Re-export the imported classes
__all__ = ['Flow', 'BatchNode', 'BatchFlow'] 