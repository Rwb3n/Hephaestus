"""
Nodes module - DEPRECATED

This module has been moved to core
Importing from nodes is deprecated and will be removed in a future version.
"""

import warnings
import sys
from pathlib import Path

# Add parent directory to path to ensure imports work
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Import from the new locations
from core.base_node import Node, NodeActionTransition
from core.flow import Flow, BatchNode, BatchFlow

# Show deprecation warning
warnings.warn(
    "Importing from nodes is deprecated. Use 'from core import Node, Flow, BatchNode, BatchFlow' instead.",
    DeprecationWarning, stacklevel=2
)

# Re-export the imported classes
__all__ = ['Node', 'NodeActionTransition', 'Flow', 'BatchNode', 'BatchFlow'] 