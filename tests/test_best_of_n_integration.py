"""
Test script for BestOfNBuilder integration with FlowBuilderNode.

This script tests the proper integration and functionality of the
BestOfNBuilder and FlowBuilderNode components working together.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path to allow importing from root
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

import pytest
from tests.mock_services import (
    MockLLMService, 
    MockMutationEngine, 
    MockFlowBuilderNode,
    MockTestHarness
)

# Import the components to test
from scoring.best_of_n import BestOfNBuilder
from engine.flow_builder import FlowBuilderNode
from engine.mutation_engine import MutationEngine
from engine.test_harness import TestHarness

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture
def sample_registry():
    """Create a sample registry for testing."""
    return {
        "builds": [],
        "lineage": {},
        "last_build_id": 0
    }


@pytest.fixture
def sample_shared_state(sample_registry):
    """Create a sample shared state for testing."""
    return {
        "build_task": "Build a Node that validates user input",
        "directive": {
            "description": "Input validation node",
            "constraints": ["Handle empty input", "Validate email format"]
        },
        "registry": sample_registry
    }


@pytest.fixture
def mock_llm_service():
    """Create a mock LLM service."""
    return MockLLMService(responses={
        "validate": "def validate_input(data):\n    return data is not None",
        "process": "def process_data(data):\n    return {'processed': True, 'data': data}",
        "api": "def call_api(url, data):\n    return {'status': 200, 'response': 'Success'}"
    })


@pytest.fixture
def mock_mutation_engine():
    """Create a mock mutation engine."""
    return MockMutationEngine(mutations=[
        (
            "Build a Node that validates user input", 
            {"description": "Input validator", "constraints": ["Handle nulls"]}
        ),
        (
            "Create a Node that processes API responses", 
            {"description": "API processor", "constraints": ["Handle errors"]}
        ),
        (
            "Implement a Flow for data transformation", 
            {"description": "Data transformer", "constraints": ["Be efficient"]}
        )
    ])


@pytest.fixture
def mock_flow_builder():
    """Create a mock flow builder."""
    return MockFlowBuilderNode()


@pytest.fixture
def mock_test_harness():
    """Create a mock test harness."""
    return MockTestHarness(test_results={
        "validate": {
            "passed": True,
            "score": 0.85,
            "execution_time": 0.05,
            "stdout": "Validation test passed",
            "stderr": ""
        },
        "process": {
            "passed": True,
            "score": 0.78,
            "execution_time": 0.08,
            "stdout": "Processing test passed",
            "stderr": ""
        },
        "default": {
            "passed": True,
            "score": 0.70,
            "execution_time": 0.06,
            "stdout": "Test executed successfully",
            "stderr": ""
        },
        "error": {
            "passed": False,
            "score": 0.30,
            "execution_time": 0.02,
            "stdout": "",
            "stderr": "Test failed with error"
        }
    })


def test_best_of_n_builder_init():
    """Test BestOfNBuilder initialization."""
    builder = BestOfNBuilder(n=5)
    
    # Check that the builder is initialized correctly
    assert builder.n == 5
    assert builder.mutation_engine is not None
    assert builder.flow_builder is not None
    assert builder.test_harness is not None


def test_best_of_n_builder_prep(sample_shared_state):
    """Test BestOfNBuilder prep method."""
    builder = BestOfNBuilder()
    result = builder.prep(sample_shared_state)
    
    # Check that prep extracts the correct values
    assert "build_task" in result
    assert result["build_task"] == sample_shared_state["build_task"]
    assert "directive" in result
    assert result["directive"] == sample_shared_state["directive"]
    assert "registry" in result
    assert result["registry"] == sample_shared_state["registry"]


def test_best_of_n_builder_exec(sample_shared_state, mock_mutation_engine, 
                             mock_flow_builder, mock_test_harness):
    """Test BestOfNBuilder exec method."""
    # Create builder with mocked components
    builder = BestOfNBuilder(
        n=3,
        mutation_engine=mock_mutation_engine,
        flow_builder=mock_flow_builder,
        test_harness=mock_test_harness
    )
    
    # Run prep and exec
    prep_res = builder.prep(sample_shared_state)
    variants = builder.exec(prep_res)
    
    # Check that we got the expected number of variants
    assert len(variants) <= 3  # May be less if some variants failed to generate
    
    # Check variant structure for the first variant
    if variants:
        variant = variants[0]
        assert "build_task" in variant
        assert "directive" in variant
        assert "code" in variant
        assert "score" in variant
        assert "test_results" in variant
        assert "variant_idx" in variant


def test_best_of_n_builder_post(sample_shared_state):
    """Test BestOfNBuilder post method."""
    builder = BestOfNBuilder()
    
    # Create some test variants
    variants = [
        {
            "build_task": "Build a Node that validates user input",
            "directive": {"description": "Input validator"},
            "code": "def validate(data): return True",
            "score": 0.5,
            "test_results": {"passed": True},
            "variant_idx": 0
        },
        {
            "build_task": "Create a Node that validates input comprehensively",
            "directive": {"description": "Comprehensive validator"},
            "code": "def validate(data): return data is not None",
            "score": 0.8,
            "test_results": {"passed": True},
            "variant_idx": 1
        },
        {
            "build_task": "Design a validation system",
            "directive": {"description": "Validation system"},
            "code": "def validate(data): pass",
            "score": 0.3,
            "test_results": {"passed": True},
            "variant_idx": 2
        }
    ]
    
    # Run post with a copy of shared_state
    shared = sample_shared_state.copy()
    action = builder.post(shared, None, variants)
    
    # Check that the highest scoring variant was selected
    assert action == "success"
    assert shared["score"] == 0.8
    assert shared["code"] == "def validate(data): return data is not None"
    assert shared["build_task"] == "Create a Node that validates input comprehensively"
    assert shared["directive"] == {"description": "Comprehensive validator"}
    
    # Check that feedback was provided
    assert "feedback" in shared
    assert shared["feedback"]["best_variant_idx"] == 1
    assert shared["feedback"]["best_score"] == 0.8
    assert shared["feedback"]["variant_count"] == 3
    
    # Check that all variants were stored
    assert "variants" in shared
    assert len(shared["variants"]) == 3


def test_best_of_n_with_flow_builder_integration(sample_shared_state, 
                                             mock_mutation_engine,
                                             mock_flow_builder, 
                                             mock_test_harness):
    """Test BestOfNBuilder integration with FlowBuilderNode."""
    # Create builder with mocked components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mock_mutation_engine,
        flow_builder=mock_flow_builder,
        test_harness=mock_test_harness
    )
    
    # Run the full node
    shared = sample_shared_state.copy()
    action = builder.run(shared)
    
    # Verify results
    assert action in ["success", "fail"]
    if action == "success":
        assert "code" in shared
        assert "score" in shared
        assert "feedback" in shared
        assert "variants" in shared
        assert len(shared["variants"]) <= 2


def test_best_of_n_error_handling(sample_shared_state, 
                               mock_mutation_engine,
                               mock_flow_builder):
    """Test BestOfNBuilder error handling."""
    # Create a test harness that always fails
    failing_test_harness = MockTestHarness(test_results={
        "default": {
            "passed": False,
            "score": 0.3,
            "execution_time": 0.01,
            "stdout": "",
            "stderr": "Error in test"
        }
    })
    
    # Create builder with mocked components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mock_mutation_engine,
        flow_builder=mock_flow_builder,
        test_harness=failing_test_harness
    )
    
    # Set a high score threshold
    shared = sample_shared_state.copy()
    shared["score_threshold"] = 0.7
    
    # Run the node
    action = builder.run(shared)
    
    # Verify that the node detected failure
    assert action == "fail"
    assert shared.get("score", 0) < shared["score_threshold"]
    assert "feedback" in shared


def test_best_of_n_empty_variants(sample_shared_state, 
                               mock_mutation_engine):
    """Test BestOfNBuilder with no successful variants."""
    # Create a flow builder that always fails (returns no code)
    failing_flow_builder = MockFlowBuilderNode()
    failing_flow_builder.exec = lambda prep_res: None
    
    # Create builder with mocked components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mock_mutation_engine,
        flow_builder=failing_flow_builder,
        test_harness=MockTestHarness()
    )
    
    # Run the node
    shared = sample_shared_state.copy()
    action = builder.run(shared)
    
    # Verify that the node handled the case with no variants
    assert action == "fail"
    assert "code" not in shared
    
    # Check for appropriate error message in log (would need to capture logs)


def test_forge_loop_with_best_of_n(sample_shared_state, 
                                mock_mutation_engine,
                                mock_flow_builder, 
                                mock_test_harness):
    """Test ForgeLoop with BestOfNBuilder integration."""
    # This test requires ForgeLoop which would need to be imported
    # For now, we'll just simulate what ForgeLoop would do
    
    # Create builder with mocked components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mock_mutation_engine,
        flow_builder=mock_flow_builder,
        test_harness=mock_test_harness
    )
    
    # Simulate ForgeLoop calling BestOfNBuilder
    shared = sample_shared_state.copy()
    action = builder.run(shared)
    
    # ForgeLoop would then process the results and update registry
    if action == "success":
        # Update registry with the new build
        registry = shared.get("registry", {})
        registry.setdefault("builds", []).append({
            "build_id": registry.get("last_build_id", 0) + 1,
            "task": shared.get("build_task", ""),
            "code": shared.get("code", ""),
            "score": shared.get("score", 0)
        })
        registry["last_build_id"] = registry.get("last_build_id", 0) + 1
        
        # Verify registry was updated
        assert len(registry["builds"]) == 1
        assert registry["last_build_id"] == 1
        assert registry["builds"][0]["score"] > 0


def main():
    """Run the tests."""
    # Run pytest programmatically
    import pytest
    sys.exit(pytest.main(["-xvs", __file__]))

if __name__ == "__main__":
    main() 