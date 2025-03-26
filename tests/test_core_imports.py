"""
Test script for core imports after directory reorganization.

This script verifies that both the new imports from core
and the legacy imports from nodes and registry work correctly
with appropriate deprecation warnings.
"""

import os
import sys
import warnings
import logging
from pathlib import Path

# Add parent directory to path to ensure imports work
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_new_imports():
    """Test imports from the new core module."""
    try:
        from core import Node, Flow, BatchNode, BatchFlow, Registry
        
        # Test creating instances
        node = Node()
        flow = Flow(start=node)
        batch_node = BatchNode()
        batch_flow = BatchFlow(start=node)
        registry = Registry()
        
        logger.info("✅ New imports from core module successful")
        return True
    except Exception as e:
        logger.error(f"❌ New imports failed: {str(e)}")
        return False

def test_legacy_node_imports():
    """Test imports from the legacy nodes module."""
    try:
        # Filter deprecation warnings for this test
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", DeprecationWarning)
            
            from nodes import Node, Flow, BatchNode, BatchFlow
            
            # Test creating instances
            node = Node()
            flow = Flow(start=node)
            batch_node = BatchNode()
            batch_flow = BatchFlow(start=node)
            
            # Check for deprecation warnings
            if any(issubclass(warning.category, DeprecationWarning) for warning in w):
                logger.info("✅ Legacy nodes import successful with deprecation warning")
            else:
                logger.warning("⚠️ Legacy nodes import successful but no deprecation warning")
            
            return True
    except Exception as e:
        logger.error(f"❌ Legacy nodes imports failed: {str(e)}")
        return False

def test_legacy_registry_imports():
    """Test imports from the legacy registry module."""
    try:
        # Filter deprecation warnings for this test
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", DeprecationWarning)
            
            from registry import Registry
            
            # Test creating instance
            registry = Registry()
            
            # Check for deprecation warnings
            if any(issubclass(warning.category, DeprecationWarning) for warning in w):
                logger.info("✅ Legacy registry import successful with deprecation warning")
            else:
                logger.warning("⚠️ Legacy registry import successful but no deprecation warning")
            
            return True
    except Exception as e:
        logger.error(f"❌ Legacy registry imports failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    logger.info("Testing imports after directory reorganization...")
    
    # Run tests
    results = [
        ("New imports from core", test_new_imports()),
        ("Legacy imports from nodes", test_legacy_node_imports()),
        ("Legacy imports from registry", test_legacy_registry_imports()),
    ]
    
    # Print results
    logger.info("\n" + "="*50)
    logger.info("IMPORT TEST RESULTS:")
    logger.info("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {name}")
        all_passed = all_passed and passed
    
    logger.info("="*50)
    if all_passed:
        logger.info("✅ All import tests passed!")
    else:
        logger.error("❌ Some tests failed. See logs for details.")
    
    return all_passed

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 