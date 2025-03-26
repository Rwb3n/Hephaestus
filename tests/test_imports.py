"""
Test script to verify imports after directory reorganization.

This script tests both the new import paths and the compatibility
imports to ensure everything works correctly.
"""

import os
import sys
import logging
import warnings
import traceback
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ImportTest")

# Filter out deprecation warnings for this test
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Track all tests and their status
results = {"passed": [], "failed": []}

def run_test(name, test_func):
    """Run a test and log the result."""
    try:
        test_func()
        logger.info(f"✅ {name} - PASSED")
        results["passed"].append(name)
    except Exception as e:
        logger.error(f"❌ {name} - FAILED: {str(e)}")
        logger.error(traceback.format_exc())
        results["failed"].append(name)

# Tests for core imports
def test_core_node_imports():
    """Test importing Node from core module."""
    from core.base_node import Node
    from core.flow import Flow, BatchNode, BatchFlow
    # Verify they're usable
    node = Node()
    flow = Flow(start=node)
    batch_node = BatchNode()
    batch_flow = BatchFlow(start=node)

def test_core_registry_imports():
    """Test importing Registry from core module."""
    from core.registry import Registry
    # Verify it's usable
    registry = Registry()

# Tests for old compatibility imports
def test_nodes_compatibility_imports():
    """Test compatibility imports from nodes module."""
    from nodes.base_node import Node
    from nodes.flow import Flow, BatchNode, BatchFlow
    # Verify they're usable
    node = Node()
    flow = Flow(start=node)
    batch_node = BatchNode()
    batch_flow = BatchFlow(start=node)

def test_registry_compatibility_imports():
    """Test compatibility imports from registry module."""
    from registry.registry import Registry
    # Verify it's usable
    registry = Registry()

# Tests for scoring module imports
def test_scoring_direct_imports():
    """Test direct imports from scoring module."""
    from scoring import BestOfNBuilder, Scorer, TestHarness, ExtractImports
    # Verify they're usable
    best_of_n = BestOfNBuilder()
    scorer = Scorer()
    test_harness = TestHarness()
    extract_imports = ExtractImports()

def test_scoring_submodule_imports():
    """Test imports from scoring submodules."""
    from scoring.best_of_n import BestOfNBuilder
    from scoring.scorer import Scorer
    from scoring.test_harness import TestHarness, ExtractImports
    # Verify they're usable
    best_of_n = BestOfNBuilder()
    scorer = Scorer()
    test_harness = TestHarness()
    extract_imports = ExtractImports()

def test_scoring_implementation_imports():
    """Test imports directly from implementation modules."""
    from scoring.scorer.scorer import Scorer
    from scoring.test_harness.harness import TestHarness, ExtractImports
    # Verify they're usable
    scorer = Scorer()
    test_harness = TestHarness()
    extract_imports = ExtractImports()

def test_scoring_compatibility_imports():
    """Test compatibility imports from old locations."""
    from scoring.scoring import Scorer, BestOfNBuilder
    from scoring.test_harness import TestHarness, ExtractImports
    # Verify they're usable
    best_of_n = BestOfNBuilder()
    scorer = Scorer()
    test_harness = TestHarness()
    extract_imports = ExtractImports()

def main():
    """Run all import tests."""
    # Print the Python path for debugging
    logger.info(f"Python path: {sys.path}")
    
    # Core imports
    run_test("Core Node Imports", test_core_node_imports)
    run_test("Core Registry Imports", test_core_registry_imports)
    
    # Compatibility imports
    run_test("Nodes Compatibility Imports", test_nodes_compatibility_imports)
    run_test("Registry Compatibility Imports", test_registry_compatibility_imports)
    
    # Scoring imports
    run_test("Scoring Direct Imports", test_scoring_direct_imports)
    run_test("Scoring Submodule Imports", test_scoring_submodule_imports)
    run_test("Scoring Implementation Imports", test_scoring_implementation_imports)
    run_test("Scoring Compatibility Imports", test_scoring_compatibility_imports)
    
    # Summary
    total = len(results["passed"]) + len(results["failed"])
    logger.info(f"Import Tests Summary: {len(results['passed'])}/{total} passed")
    
    if results["failed"]:
        logger.error(f"Failed tests: {', '.join(results['failed'])}")
        return 1
    else:
        logger.info("All import tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 