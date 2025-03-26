"""
Test runner for Hephaestus.

This script runs all available tests and reports the results.
"""

import os
import sys
import importlib
import logging
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

def run_test_module(module_name: str) -> bool:
    """
    Run tests from a single module.
    
    Args:
        module_name: Name of the test module
        
    Returns:
        True if tests pass, False otherwise
    """
    try:
        logger.info(f"Running tests from {module_name}...")
        module = importlib.import_module(module_name)
        
        # Check if the module has a main function
        if hasattr(module, "main"):
            logger.info(f"Running {module_name}.main()")
            module.main()
            return True
        else:
            logger.warning(f"{module_name} has no main() function")
            return False
            
    except Exception as e:
        logger.error(f"Error running tests from {module_name}: {e}")
        return False

def discover_test_modules():
    """
    Discover all test modules in the tests directory.
    
    Returns:
        List of test module names
    """
    tests_dir = Path(__file__).parent
    test_modules = []
    
    for file in tests_dir.glob("test_*.py"):
        if file.name != "run_tests.py":
            module_name = f"tests.{file.stem}"
            test_modules.append(module_name)
    
    return test_modules

def run_all_tests():
    """
    Run all tests and report results.
    
    Returns:
        True if all tests pass, False otherwise
    """
    logger.info("Starting test run...")
    
    # Create output directory for test results
    os.makedirs("tests/output", exist_ok=True)
    
    # Discover test modules
    test_modules = discover_test_modules()
    
    if not test_modules:
        logger.warning("No test modules found")
        return False
    
    logger.info(f"Found {len(test_modules)} test modules: {test_modules}")
    
    # Run each test module
    results = {}
    for module_name in test_modules:
        results[module_name] = run_test_module(module_name)
    
    # Report results
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS:")
    logger.info("="*50)
    
    all_passed = True
    for module_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {module_name}")
        all_passed = all_passed and passed
    
    logger.info("="*50)
    if all_passed:
        logger.info("✅ All tests passed!")
    else:
        logger.error("❌ Some tests failed. See logs for details.")
    
    return all_passed

if __name__ == "__main__":
    """Run all tests and exit with appropriate status code."""
    success = run_all_tests()
    sys.exit(0 if success else 1) 