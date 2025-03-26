"""
Base Node module - DEPRECATED

This module has been moved to core.base_node
Importing from nodes.base_node is deprecated and will be removed in a future version.
"""

import warnings
import sys
from pathlib import Path

# Add parent directory to path to ensure imports work
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Import from the new location
from core.base_node import Node, NodeActionTransition

# Show deprecation warning
warnings.warn(
    "Importing from nodes.base_node is deprecated. Use 'from core.base_node import Node' instead.",
    DeprecationWarning, stacklevel=2
)

# Re-export the imported classes
__all__ = ['Node', 'NodeActionTransition'] 