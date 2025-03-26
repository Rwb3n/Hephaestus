"""
Test script for the consolidated BestOfNBuilder implementation.

This script verifies that the consolidated BestOfNBuilder works
with both direct imports and compatibility imports.
"""

import os
import sys
import logging
import warnings
from pathlib import Path

# Add parent directory to path to allow importing from root
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import mock services
from tests.mock_services import (
    MockMutationEngine,
    MockFlowBuilderNode,
    MockTestHarness
)

def test_consolidated_import():
    """Test direct import of consolidated BestOfNBuilder."""
    # Import the consolidated implementation
    from scoring.best_of_n import BestOfNBuilder
    
    # Create a builder with mock components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=MockMutationEngine(),
        flow_builder=MockFlowBuilderNode(),
        test_harness=MockTestHarness()
    )
    
    # Verify initialization
    assert builder.n == 2
    assert builder.mutation_engine is not None
    assert builder.flow_builder is not None
    assert builder.test_harness is not None
    
    logger.info("Direct import test passed")
    return True

def test_compatibility_import():
    """Test compatibility import from engine module."""
    # Filter deprecation warnings for this test
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    # Import from the deprecated location
    from engine import BestOfNBuilder
    
    # Create a builder with mock components
    builder = BestOfNBuilder(
        n=3,
        mutation_engine=MockMutationEngine(),
        flow_builder=MockFlowBuilderNode(),
        test_harness=MockTestHarness()
    )
    
    # Verify initialization
    assert builder.n == 3
    assert builder.mutation_engine is not None
    assert builder.flow_builder is not None
    assert builder.test_harness is not None
    
    logger.info("Compatibility import test passed")
    return True

def test_basic_functionality():
    """Test basic functionality of the consolidated BestOfNBuilder."""
    from scoring.best_of_n import BestOfNBuilder
    
    # Create mock components
    mutation_engine = MockMutationEngine()
    flow_builder = MockFlowBuilderNode()
    test_harness = MockTestHarness()
    
    # Create the builder
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mutation_engine,
        flow_builder=flow_builder,
        test_harness=test_harness
    )
    
    # Create shared data
    shared = {
        "build_task": "Create a validation node",
        "directive": {"constraints": ["Handle null values"]},
        "score_threshold": 0.7
    }
    
    # Run the builder
    action = builder.run(shared)
    
    # Verify results
    assert action in ["success", "fail"]
    assert "variants" in shared
    assert "feedback" in shared
    
    logger.info(f"Basic functionality test result: {action}")
    return True

def main():
    """Run all tests."""
    tests = [
        test_consolidated_import,
        test_compatibility_import,
        test_basic_functionality
    ]
    
    results = []
    for test in tests:
        try:
            results.append((test.__name__, test()))
        except Exception as e:
            logger.error(f"Error in {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Report results
    logger.info("\n" + "="*50)
    logger.info("CONSOLIDATION TEST RESULTS:")
    logger.info("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {name}")
        all_passed = all_passed and passed
    
    logger.info("="*50)
    if all_passed:
        logger.info("✅ All consolidation tests passed!")
    else:
        logger.error("❌ Some tests failed. See logs for details.")
    
    return all_passed

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 