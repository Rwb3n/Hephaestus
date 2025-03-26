import logging
import re
import os
import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple

from nodes.base_node import Node
from services import TemplateLoader, OpenAIService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class FlowBuilderNode(Node):
    """
    FlowBuilderNode synthesizes executable Python code for Nodes and Flows.
    
    It translates natural language directives into code implementations, 
    following the constraints and structure of the Hephaestus system.
    """
    
    def __init__(self, llm_service=None, template_loader=None):
        """
        Initialize the FlowBuilderNode.
        
        Args:
            llm_service: LLM service for code generation (if None, uses placeholders)
            template_loader: Template loader for prompt templates
        """
        super().__init__(max_retries=2)  # Allow retries for LLM calls
        self.logger = logging.getLogger("FlowBuilderNode")
        
        # Initialize services
        self.llm_service = llm_service
        if self.llm_service is None:
            try:
                self.llm_service = OpenAIService()
                self.logger.info("Using OpenAI service as default LLM service")
            except Exception as e:
                self.logger.warning(f"Could not initialize OpenAI service: {e}. Using placeholder code.")
        
        # Initialize template loader
        self.template_loader = template_loader
        if self.template_loader is None:
            try:
                self.template_loader = TemplateLoader()
                self.logger.info("Using default template loader")
            except Exception as e:
                self.logger.warning(f"Could not initialize template loader: {e}")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare for code generation by extracting task and directive.
        
        Args:
            shared: The shared data store
            
        Returns:
            Dictionary with task and directive
        """
        # Get task details
        build_task = shared.get("build_task", "")
        directive = shared.get("directive", {})
        
        # Get current variant if in a batch process
        variant_idx = self.params.get("variant_idx", 0)
        variants = shared.get("variants", [])
        
        if variants and variant_idx < len(variants):
            variant = variants[variant_idx]
            build_task = variant.get("task", build_task)
            directive = variant.get("directive", directive)
        
        # Get past successful builds from registry for reference
        registry = shared.get("registry", {})
        
        # Get existing code to reference (if available)
        existing_code = shared.get("existing_code", {})
        
        return {
            "build_task": build_task,
            "directive": directive,
            "registry": registry,
            "existing_code": existing_code
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> str:
        """
        Generate code based on the task and directive.
        
        Args:
            prep_res: Dictionary with task and directive
            
        Returns:
            Generated code as a string
        """
        build_task = prep_res.get("build_task", "")
        directive = prep_res.get("directive", {})
        registry = prep_res.get("registry", {})
        existing_code = prep_res.get("existing_code", {})
        
        self.logger.info(f"Generating code for task: {build_task}")
        
        # Determine if we're building a Node or a Flow
        is_flow = False
        node_type = "Node"
        
        if "flow" in build_task.lower():
            is_flow = True
            node_type = "Flow"
        
        # If we have an LLM service, use it to generate code
        if self.llm_service and self.template_loader:
            try:
                # Use asyncio to run the async method
                try:
                    # Try to use the event loop if it exists
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    # Create a new event loop if one doesn't exist
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Determine which template to use
                template_name = "flow_builder" if is_flow else "node_generation"
                
                # Check if we have any reference implementations
                reference_nodes = ""
                if existing_code:
                    # Get up to 3 relevant examples
                    reference_nodes = "\n\n".join(list(existing_code.values())[:3])
                
                # Prepare template context
                context = {
                    "directive": str(directive),
                    "task_description": build_task,
                    "node_type": node_type,
                    "reference_nodes": reference_nodes,
                }
                
                # Render the template
                prompt = self.template_loader.render_template(template_name, **context)
                
                # Generate code
                code = loop.run_until_complete(
                    self.llm_service.generate_code(
                        task_description=build_task,
                        language="python",
                        max_length=200,  # Enforce 200 line limit
                        requirements=str(directive),
                        reference_code=reference_nodes
                    )
                )
                
                return code
                
            except Exception as e:
                self.logger.error(f"Error generating code with LLM: {e}")
                # Fall back to placeholder
                return self._generate_placeholder_code(build_task, directive)
        else:
            # Generate placeholder code
            code = self._generate_placeholder_code(build_task, directive)
            return code
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: str) -> str:
        """
        Process the generated code and update the shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: Generated code
            
        Returns:
            Action string for flow control
        """
        # Store the generated code
        shared["code"] = exec_res
        
        # Extract class name for better identification
        class_name = self._extract_class_name(exec_res)
        if class_name:
            shared["class_name"] = class_name
            self.logger.info(f"Generated {class_name} implementation")
        
        # Store build metadata
        variant_idx = self.params.get("variant_idx", 0)
        shared["variant_idx"] = variant_idx
        
        # Save to disk if save_path is provided
        save_path = shared.get("save_path")
        if save_path:
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Write code to file
                with open(save_path, "w") as f:
                    f.write(exec_res)
                    
                self.logger.info(f"Saved generated code to {save_path}")
                shared["file_path"] = save_path
            except Exception as e:
                self.logger.error(f"Error saving code to {save_path}: {e}")
        
        self.logger.info(f"Code generation complete for variant {variant_idx}")
        return "default"
    
    def _extract_class_name(self, code: str) -> Optional[str]:
        """
        Extract the class name from generated code.
        
        Args:
            code: The generated code
            
        Returns:
            Class name if found, None otherwise
        """
        # Look for class definition
        match = re.search(r"class\s+(\w+)\s*\(", code)
        if match:
            return match.group(1)
        return None
    
    def _generate_placeholder_code(self, build_task: str, directive: Dict[str, Any]) -> str:
        """
        Generate placeholder code based on the task.
        
        In a real implementation, this would call an LLM to generate code.
        
        Args:
            build_task: The task description
            directive: The directive dictionary
            
        Returns:
            Placeholder code as a string
        """
        # Extract key terms from the build task
        node_match = re.search(r"(Node|Flow) that (.+)", build_task, re.IGNORECASE)
        
        class_name = "CustomNode"
        description = "performs a custom operation"
        
        if node_match:
            component_type = node_match.group(1)
            description = node_match.group(2)
            
            # Create a class name from the description
            words = re.findall(r'\b[A-Za-z]+\b', description)
            if words:
                class_name = "".join(w.capitalize() for w in words[:3]) + component_type
        
        # Generate placeholder code
        code = f"""import logging
from typing import Dict, Any, Optional

from nodes.base_node import Node

class {class_name}(Node):
    \"\"\"
    {class_name} {description}.
    
    Built by Hephaestus for task: {build_task}
    \"\"\"
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("{class_name}")
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        \"\"\"
        Prepare data for processing.
        
        Args:
            shared: The shared data store
            
        Returns:
            Data to be processed
        \"\"\"
        # Implement preparation logic here
        data = shared.get("data", None)
        return data
    
    def exec(self, prep_res: Any) -> Any:
        \"\"\"
        Execute the main logic.
        
        Args:
            prep_res: Result from prep()
            
        Returns:
            Processing result
        \"\"\"
        # Implement main logic here
        self.logger.info(f"Processing data: {{prep_res}}")
        result = f"Processed: {{prep_res}}"
        return result
    
    def post(self, shared: Dict[str, Any], prep_res: Any, exec_res: Any) -> Optional[str]:
        \"\"\"
        Post-process and store results.
        
        Args:
            shared: The shared data store
            prep_res: Result from prep()
            exec_res: Result from exec()
            
        Returns:
            Action string for flow control
        \"\"\"
        # Implement post-processing logic here
        shared["result"] = exec_res
        return "default"

def main():
    \"\"\"
    Test the node with sample data.
    \"\"\"
    node = {class_name}()
    shared = {{"data": "Hello, world!"}}
    action = node.run(shared)
    print(f"Action: {{action}}")
    print(f"Result: {{shared.get('result')}}")

if __name__ == "__main__":
    main()
"""
        return code

class DirectiveLoader(Node):
    """
    Helper node to load directives into the shared store.
    """
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Get build task and registry."""
        return {
            "build_task": shared.get("build_task", ""),
            "registry": shared.get("registry", {})
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> Dict[str, Any]:
        """Create a directive based on build task."""
        build_task = prep_res.get("build_task", "")
        
        directive = {
            "goal": "Expand Hephaestus' capabilities",
            "constraints": {
                "max_lines_per_file": 200,
                "require_registry_logging": True
            },
            "reward_criteria": ["modularity", "reusability", "fault_tolerance"]
        }
        
        return directive
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: Dict[str, Any]) -> str:
        """Store directive in shared store."""
        shared["directive"] = exec_res
        return "default"
