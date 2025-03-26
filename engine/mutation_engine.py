import random
import copy
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

from nodes.base_node import Node

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MutationEngine(Node):
    """
    MutationEngine introduces variation into tasks and directives.
    
    It controls the amount of entropy in the generation process and
    helps explore the solution space without derailing the core goal.
    """
    
    def __init__(self, entropy: float = 0.3):
        """
        Initialize the MutationEngine with mutation options.
        
        Args:
            entropy: Float between 0-1 controlling mutation frequency
        """
        super().__init__()
        self.logger = logging.getLogger("MutationEngine")
        self.entropy = entropy
        
        self.verb_swaps = {
            "build": ["forge", "construct", "assemble", "fabricate"],
            "extract": ["harvest", "pull", "gather", "retrieve"],
            "summarize": ["distill", "reduce", "interpret", "compress"],
            "analyze": ["study", "dissect", "inspect", "scrutinize"],
        }
        self.adjective_injections = [
            "minimal", "robust", "async-compatible", "fault-tolerant", "reusable"
        ]

    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare for mutation by extracting task and directive.
        
        Args:
            shared: The shared data store containing task and directive
            
        Returns:
            Dictionary with task and directive
        """
        task = shared.get("build_task", "")
        directive = shared.get("directive", {})
        
        return {
            "task": task,
            "directive": directive
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate mutations of the task and directive.
        
        Args:
            prep_res: Dictionary with task and directive
            
        Returns:
            List of dictionaries with mutated tasks and directives
        """
        task = prep_res.get("task", "")
        directive = prep_res.get("directive", {})
        
        # Number of variants to generate
        n_variants = self.params.get("n_variants", 3)
        
        # Generate variants
        variants = []
        
        # Always include the original as one variant
        variants.append({
            "task": task,
            "directive": copy.deepcopy(directive)
        })
        
        # Generate n-1 mutations
        for _ in range(n_variants - 1):
            mutated_task = self.mutate_task(task)
            mutated_directive = self.mutate_directive(directive)
            
            variants.append({
                "task": mutated_task,
                "directive": mutated_directive
            })
        
        self.logger.info(f"Generated {len(variants)} variants")
        return variants
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: List[Dict[str, Any]]) -> str:
        """
        Process the mutations and update the shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: List of mutations
            
        Returns:
            Action string for flow control
        """
        # Store the variants for use by downstream nodes
        shared["variants"] = exec_res
        
        return "default"
    
    def mutate_task(self, task: str) -> str:
        """
        Introduce variation into a task description.
        
        Args:
            task: Task description string
            
        Returns:
            Mutated task description
        """
        words = task.split()
        mutated = []

        for word in words:
            lower = word.lower()
            # Only swap verbs based on entropy setting
            if lower in self.verb_swaps and random.random() < self.entropy:
                mutated.append(random.choice(self.verb_swaps[lower]))
            else:
                mutated.append(word)

        # Random adjective injection
        if random.random() < self.entropy:
            idx = random.randint(1, len(mutated)-1)
            adj = random.choice(self.adjective_injections)
            mutated.insert(idx, adj)
        
        mutated_task = " ".join(mutated)
        self.logger.debug(f"Mutated task: {task} -> {mutated_task}")
        return mutated_task

    def mutate_directive(self, directive: Dict[str, Any]) -> Dict[str, Any]:
        """
        Introduce variation into a directive.
        
        Args:
            directive: Directive dictionary
            
        Returns:
            Mutated directive
        """
        directive = copy.deepcopy(directive)

        # Optional mutation of constraints
        if "constraints" in directive and random.random() < self.entropy:
            constraints = directive["constraints"]
            
            if "max_lines_per_file" in constraints and random.random() < self.entropy:
                current = constraints["max_lines_per_file"]
                # Adjust by up to 20% in either direction
                new_value = int(current * (0.8 + 0.4 * random.random()))
                # Keep within reasonable bounds
                new_value = max(50, min(new_value, 200))
                constraints["max_lines_per_file"] = new_value

        # Optional mutation of reward criteria
        if "reward_criteria" in directive and random.random() < self.entropy:
            potential_criteria = [
                "modularity", "clarity", "speed", "elegance", 
                "robustness", "testability", "maintainability"
            ]
            
            # Add a new criterion
            existing = set(directive["reward_criteria"])
            new_criteria = [c for c in potential_criteria if c not in existing]
            
            if new_criteria and random.random() < self.entropy:
                directive["reward_criteria"].append(random.choice(new_criteria))
            
            # Potentially reorder criteria
            if random.random() < self.entropy:
                random.shuffle(directive["reward_criteria"])

        return directive
