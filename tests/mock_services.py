"""
Mock implementations of Hephaestus services for testing.

This module provides mock versions of the key services used in Hephaestus,
allowing for deterministic testing without external dependencies.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple

from services.llm_service import LLMService
from engine.mutation_engine import MutationEngine
from engine.flow_builder import FlowBuilderNode
from engine.test_harness import TestHarness

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockLLMService(LLMService):
    """
    Mock implementation of LLMService for testing.
    
    Returns predefined responses based on the request.
    """
    
    def __init__(self, responses: Dict[str, str] = None):
        """
        Initialize the mock LLM service.
        
        Args:
            responses: Dictionary mapping keywords to predefined responses
        """
        super().__init__(model="mock-model", api_key="mock-key")
        self.responses = responses or {
            "code": "def mock_function():\n    return 'mocked'",
            "default": "Mock response"
        }
        self.logger = logging.getLogger("MockLLMService")
        self.call_history = []
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a mock response based on the prompt.
        
        Args:
            prompt: The prompt string
            **kwargs: Additional parameters
            
        Returns:
            A predefined response string
        """
        # Log the call
        self.call_history.append({"prompt": prompt, "kwargs": kwargs})
        self.logger.debug(f"Mock LLM called with prompt: {prompt[:50]}...")
        
        # Find matching response
        for key, response in self.responses.items():
            if key.lower() in prompt.lower():
                return response
                
        # Default response
        return self.responses.get("default", "Mock response")
        
    async def generate_with_template(self, template_name: str, **kwargs) -> str:
        """
        Generate mock response for a template.
        
        Args:
            template_name: Name of the template
            **kwargs: Template parameters
            
        Returns:
            A predefined response string
        """
        # Log the call
        self.call_history.append({"template_name": template_name, "kwargs": kwargs})
        self.logger.debug(f"Mock LLM called with template: {template_name}")
        
        # Return template-specific response if available
        if template_name in self.responses:
            return self.responses[template_name]
            
        # Otherwise return based on template name
        for key, response in self.responses.items():
            if key.lower() in template_name.lower():
                return response
                
        # Default response
        return self.responses.get("default", "Mock template response")
        
    async def generate_code(
        self, 
        task_description: str, 
        language: str = "python",
        max_length: int = None, 
        **kwargs
    ) -> str:
        """
        Generate mock code.
        
        Args:
            task_description: Description of the code to generate
            language: Programming language
            max_length: Maximum length in lines
            **kwargs: Additional parameters
            
        Returns:
            Mock code as a string
        """
        # Log the call
        self.call_history.append({
            "task_description": task_description,
            "language": language,
            "max_length": max_length,
            "kwargs": kwargs
        })
        
        self.logger.debug(f"Mock LLM called for code generation: {task_description[:50]}...")
        
        # Find matching response
        for key, response in self.responses.items():
            if key.lower() in task_description.lower():
                return response
                
        # Default code response
        return self.responses.get("code", 
            f"def mock_function():\n    # {task_description}\n    return 'mocked'"
        )


class MockMutationEngine(MutationEngine):
    """
    Mock implementation of MutationEngine for testing.
    
    Returns predefined mutations for tasks and directives.
    """
    
    def __init__(self, mutations: List[Tuple[str, Dict[str, Any]]] = None):
        """
        Initialize the mock mutation engine.
        
        Args:
            mutations: List of (task, directive) tuples to cycle through
        """
        super().__init__()
        self.mutations = mutations or [
            ("Build a Node that processes data", {"description": "Data processor"}),
            ("Create a Flow that handles user input", {"description": "Input handler"}),
            ("Develop a Node for API integration", {"description": "API connector"})
        ]
        self.current_index = 0
        self.call_history = []
        
    def mutate(self, build_task: str, directive: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Return a predefined mutation.
        
        Args:
            build_task: Original build task
            directive: Original directive
            
        Returns:
            Tuple of (mutated_task, mutated_directive)
        """
        # Log the call
        self.call_history.append({
            "original_task": build_task,
            "original_directive": directive
        })
        
        # Get next mutation
        mutation = self.mutations[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.mutations)
        
        # Customize with original task if no exact match
        if not any(m[0] == build_task for m in self.mutations):
            # Modify the task slightly
            words = build_task.split()
            if len(words) > 3:
                modified_task = " ".join(words[:2] + ["enhanced"] + words[2:])
            else:
                modified_task = f"Improved {build_task}"
                
            # Return with original directive plus a constraint
            modified_directive = directive.copy()
            constraints = modified_directive.get("constraints", [])
            modified_directive["constraints"] = constraints + ["Must be efficient"]
            
            return modified_task, modified_directive
        
        return mutation


class MockFlowBuilderNode(FlowBuilderNode):
    """
    Mock implementation of FlowBuilderNode for testing.
    
    Returns predefined code for build tasks.
    """
    
    def __init__(self, code_samples: Dict[str, str] = None):
        """
        Initialize the mock flow builder.
        
        Args:
            code_samples: Dictionary mapping task keywords to code samples
        """
        super().__init__()
        self.code_samples = code_samples or {
            "validate": """
import logging
from typing import Dict, Any

from nodes.base_node import Node

class ValidateInputNode(Node):
    \"\"\"Node that validates user input.\"\"\"
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        return shared.get("input", "")
        
    def exec(self, prep_res: Any) -> Any:
        # Simple validation
        if not prep_res:
            return {"valid": False, "error": "Input is empty"}
        return {"valid": True, "data": prep_res}
        
    def post(self, shared: Dict[str, Any], prep_res: Any, exec_res: Any) -> str:
        # Store result
        shared["validation_result"] = exec_res
        if exec_res["valid"]:
            return "valid"
        return "invalid"
""",
            "process": """
import logging
from typing import Dict, Any

from nodes.base_node import Node

class ProcessDataNode(Node):
    \"\"\"Node that processes data.\"\"\"
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        return shared.get("data", {})
        
    def exec(self, prep_res: Any) -> Any:
        # Simple processing
        if not prep_res:
            return {"success": False, "error": "No data to process"}
        
        # Process data
        result = {"processed": True, "items": len(prep_res)}
        return result
        
    def post(self, shared: Dict[str, Any], prep_res: Any, exec_res: Any) -> str:
        # Store result
        shared["processing_result"] = exec_res
        if exec_res.get("success", True):
            return "success"
        return "fail"
"""
        }
        self.call_history = []
        
    def exec(self, prep_res: Dict[str, Any]) -> str:
        """
        Generate mock code based on the build task.
        
        Args:
            prep_res: Dictionary with build task and directive
            
        Returns:
            Generated code as a string
        """
        # Log the call
        self.call_history.append(prep_res)
        
        build_task = prep_res.get("build_task", "")
        
        # Find matching code sample
        for key, code in self.code_samples.items():
            if key.lower() in build_task.lower():
                return code
                
        # Generate a default Node
        class_name = "Custom" + "".join(w.capitalize() for w in build_task.split()[:3] if w.lower() not in ["a", "the", "that"])
        if not class_name.endswith("Node"):
            class_name += "Node"
            
        return f"""
import logging
from typing import Dict, Any

from nodes.base_node import Node

class {class_name}(Node):
    \"\"\"Node generated for: {build_task}\"\"\"
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        # Basic implementation
        return shared.get("data")
        
    def exec(self, prep_res: Any) -> Any:
        # Basic processing
        return {{"result": "Processed", "data": prep_res}}
        
    def post(self, shared: Dict[str, Any], prep_res: Any, exec_res: Any) -> str:
        # Store result
        shared["result"] = exec_res
        return "default"
"""


class MockTestHarness(TestHarness):
    """
    Mock implementation of TestHarness for testing.
    
    Simulates test execution with predetermined results.
    """
    
    def __init__(self, test_results: Dict[str, Dict[str, Any]] = None):
        """
        Initialize the mock test harness.
        
        Args:
            test_results: Dictionary mapping code keywords to test results
        """
        super().__init__()
        self.test_results = test_results or {
            "default": {
                "passed": True,
                "score": 0.75,
                "execution_time": 0.05,
                "stdout": "Test executed successfully",
                "stderr": ""
            },
            "error": {
                "passed": False,
                "score": 0.2,
                "execution_time": 0.01,
                "stdout": "",
                "stderr": "SyntaxError: invalid syntax"
            }
        }
        self.call_history = []
        
    def run(self, shared: Dict[str, Any]) -> str:
        """
        Run tests on the generated code.
        
        Args:
            shared: The shared data store with code
            
        Returns:
            Action string for flow control
        """
        # Log the call
        self.call_history.append(shared)
        
        code = shared.get("code", "")
        
        # Determine test result based on code
        result = None
        for key, test_result in self.test_results.items():
            if key != "default" and key in code.lower():
                result = test_result.copy()
                break
                
        # Use default if no match
        if result is None:
            result = self.test_results["default"].copy()
            
        # Add line count and success metrics
        result["line_count"] = len(code.split("\n"))
        
        # Update shared store
        shared["test_results"] = result
        shared["score"] = result["score"]
        
        return "pass" if result["passed"] else "fail" 