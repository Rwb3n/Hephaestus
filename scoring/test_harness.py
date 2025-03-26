"""
THIS FILE IS DEPRECATED

The TestHarness implementation has been moved to scoring.test_harness module.
This file exists for backward compatibility.
"""

import warnings
from scoring.test_harness.harness import TestHarness, ExtractImports

# Show deprecation warning
warnings.warn(
    "Importing from scoring.test_harness is deprecated. "
    "Import from scoring.test_harness.harness or scoring.test_harness instead.",
    DeprecationWarning, stacklevel=2
)

__all__ = ["TestHarness", "ExtractImports"] 