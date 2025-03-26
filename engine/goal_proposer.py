import random
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

from nodes.base_node import Node

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GoalProposer(Node):
    """
    GoalProposer generates new build tasks by analyzing the registry.
    
    It serves as the system's executive function, deciding what to build next
    based on past performance and system needs.
    """

    def __init__(self):
        """Initialize the GoalProposer with task templates and options."""
        super().__init__()
        self.logger = logging.getLogger("GoalProposer")
        
        # Possible task types
        self.goal_templates = [
            "Build a Node that performs {action} on {data}",
            "Forge an async-compatible Node to {action} from {source}",
            "Construct a test harness for {component_type}",
            "Design a Flow to coordinate {function1} and {function2}",
        ]

        self.actions = ["summarize", "extract metadata", "validate", "monitor", "convert", "log"]
        self.data_types = ["JSON", "images", "URLs", "PDFs", "environment variables"]
        self.sources = ["a remote API", "a local directory", "system memory", "stdin"]
        self.components = ["LLM call nodes", "batch flows", "agent nodes"]
        self.functions = ["retrieval", "generation", "postprocessing", "evaluation"]
        
        # Tracks which directives have been reinforced
        self.reinforced_directives = set()
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare for generating a task by examining the registry.
        
        Args:
            shared: The shared data store containing registry
            
        Returns:
            Dictionary with registry data
        """
        registry = shared.get("registry", {})
        feedback = shared.get("feedback", None)
        last_directive = shared.get("directive", None)
        
        return {
            "registry": registry,
            "feedback": feedback,
            "last_directive": last_directive
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a new task based on registry analysis.
        
        Args:
            prep_res: Dictionary with registry data
            
        Returns:
            Tuple of (task description, directive dictionary)
        """
        registry = prep_res.get("registry", {})
        feedback = prep_res.get("feedback", None)
        last_directive = prep_res.get("last_directive", None)
        
        # Check feedback if available to learn from past builds
        if feedback == "reinforce" and last_directive:
            # Mark this directive as successful
            directive_key = str(last_directive)
            self.reinforced_directives.add(directive_key)
            self.logger.info(f"Reinforcing directive: {directive_key[:50]}...")
        
        # Analyze recent builds if available
        recent_builds = registry.get("builds", [])[-10:] if isinstance(registry, dict) else []
        recent_tasks = []
        
        for build in recent_builds:
            if isinstance(build, dict) and "build_task" in build:
                recent_tasks.append(build["build_task"])
        
        if not recent_tasks:
            # Cold-start prompt
            self.logger.info("No recent tasks found, using cold start task")
            return "Build a Node that logs to console", self.default_directive()
        
        # Generate a new task
        template = random.choice(self.goal_templates)
        
        task = template.format(
            action=random.choice(self.actions),
            data=random.choice(self.data_types),
            source=random.choice(self.sources),
            component_type=random.choice(self.components),
            function1=random.choice(self.functions),
            function2=random.choice(self.functions)
        )
        
        # Generate a directive
        directive = self.default_directive()
        
        # Add some variation to the directive
        if random.random() < 0.3:
            directive["constraints"]["max_lines_per_file"] = random.choice([150, 175, 200])
        
        if random.random() < 0.5:
            directive["reward_criteria"].append(random.choice([
                "efficiency", "clarity", "robustness", "testability"
            ]))
        
        self.logger.info(f"Proposed task: {task}")
        return task, directive
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: Tuple[str, Dict[str, Any]]) -> str:
        """
        Process the generated task and update the shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: Task generation results (task, directive)
            
        Returns:
            Action string for flow control
        """
        task, directive = exec_res
        
        # Update shared store with new task and directive
        shared["build_task"] = task
        shared["directive"] = directive
        
        return "default"
    
    def reinforce(self, directive: Dict[str, Any]) -> None:
        """
        Reinforce a directive that produced good results.
        
        Args:
            directive: The directive to reinforce
        """
        directive_key = str(directive)
        self.reinforced_directives.add(directive_key)
        self.logger.info(f"Explicitly reinforcing directive: {directive_key[:50]}...")
    
    def degrade(self, directive: Dict[str, Any]) -> None:
        """
        Degrade a directive that produced poor results.
        
        Args:
            directive: The directive to degrade
        """
        directive_key = str(directive)
        if directive_key in self.reinforced_directives:
            self.reinforced_directives.remove(directive_key)
        self.logger.info(f"Degrading directive: {directive_key[:50]}...")
    
    def default_directive(self) -> Dict[str, Any]:
        """
        Generate a default directive.
        
        Returns:
            Default directive dictionary
        """
        return {
            "goal": "Expand Hephaestus' capabilities",
            "constraints": {
                "max_lines_per_file": 200,
                "require_registry_logging": True
            },
            "reward_criteria": ["modularity", "reusability", "fault_tolerance"]
        }
