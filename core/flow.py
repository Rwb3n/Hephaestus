"""
Hephaestus Core Flow Module

This module contains the Flow, BatchNode, and BatchFlow classes that 
provide orchestration and batch processing capabilities for the Hephaestus system.
"""

import uuid
import logging
from typing import Any, Dict, Optional, List, Union

from core.base_node import Node

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Flow(Node):
    """
    Flow orchestrates a graph of Nodes.
    
    A Flow is itself a Node, enabling nested flows and composition.
    It executes from the start node, follows the Action returned by each node's post(),
    and continues until it reaches the end of the chain.
    
    Flows can be nested within other flows, enabling complex orchestration patterns:
    - Sequential processing (node_a >> node_b >> node_c)
    - Conditional branching (node - "action1" >> path_a, node - "action2" >> path_b)
    - Looping (node_a >> node_b >> node_a)
    """
    
    def __init__(self, start: Node, name: str = None):
        """
        Initialize a Flow with a start node.
        
        Args:
            start: The entry point node for the flow
            name: Optional name for the flow (for logging)
        """
        super().__init__()
        self.start = start
        self.name = name or f"Flow-{self.id[:8]}"
        self.logger = logging.getLogger(self.name)
        
    def run(self, shared: Dict[str, Any]) -> str:
        """
        Run the flow from the start node, following the transitions.
        
        This method overrides Node.run() to orchestrate execution of multiple nodes.
        
        Args:
            shared: The shared data store
            
        Returns:
            The final action string when the flow completes
        """
        self.logger.info(f"Starting flow execution")
        
        # Prepare the flow - run any prep logic this flow has itself
        # This is useful for nested flows that need setup
        prep_res = self.prep(shared)
        
        # Start from the first node
        current_node = self.start
        last_action = None
        
        # Track visited nodes to detect cycles
        visited = set()
        
        while current_node:
            self.logger.debug(f"Executing node {type(current_node).__name__}")
            
            # If this is a flow, let it run its own orchestration
            if isinstance(current_node, Flow) and current_node != self:
                action = current_node.run(shared)
            else:
                # Otherwise run a single node
                action = current_node.run(shared)
            
            self.logger.debug(f"Node returned action: {action}")
            last_action = action
            
            # Find the next node based on the action
            if action not in current_node.successors:
                self.logger.info(f"Flow complete - action {action} has no successor")
                break
                
            next_node = current_node.successors[action]
            
            # Basic cycle detection - in production this should be more sophisticated
            node_id = id(next_node)
            if node_id in visited:
                self.logger.warning(f"Cycle detected in flow: revisiting node {type(next_node).__name__}")
                # In a production system, you might have max_cycles or other controls
            
            visited.add(node_id)
            current_node = next_node
        
        # Run this flow's post logic - this is useful for nested flows
        # where the parent flow needs to process results
        action = self.post(shared, prep_res, last_action)
        
        self.logger.info(f"Flow execution completed with action: {action}")
        return action if action is not None else "default"
    
    def __str__(self) -> str:
        """String representation of the flow."""
        return f"{self.name}"


class BatchNode(Node):
    """
    BatchNode processes items in batches.
    
    Extends Node with batched execution for large datasets or multiple items
    that need similar processing. The prep() method returns an iterable, and
    the exec() method is called once for each item in that iterable.
    """
    
    def prep(self, shared: Dict[str, Any]) -> List[Any]:
        """
        Prepare a batch of items for processing.
        
        Should return an iterable.
        
        Args:
            shared: The shared data store
            
        Returns:
            An iterable of items to process
        """
        return []
    
    def exec(self, item: Any) -> Any:
        """
        Process a single item in the batch.
        
        Called once per item returned by prep().
        
        Args:
            item: A single item from the batch
            
        Returns:
            Result for this item
        """
        return item
    
    def post(self, shared: Dict[str, Any], prep_res: List[Any], exec_res_list: List[Any]) -> Optional[str]:
        """
        Post-process the batch of results.
        
        Args:
            shared: The shared data store
            prep_res: The original batch of items from prep()
            exec_res_list: List of results from exec() for each item
            
        Returns:
            Action string to determine the next node
        """
        return "default"
    
    def run(self, shared: Dict[str, Any]) -> str:
        """
        Run the batch node, processing each item in the batch.
        
        Args:
            shared: The shared data store
            
        Returns:
            Action string from post()
        """
        prep_res = self.prep(shared)
        
        # Process each item in the batch
        exec_res_list = []
        for item in prep_res:
            self.cur_retry = 0
            while self.cur_retry < self.max_retries:
                try:
                    result = self.exec(item)
                    exec_res_list.append(result)
                    break
                except Exception as e:
                    self.logger.error(f"Batch item execution failed (attempt {self.cur_retry+1}/{self.max_retries}): {str(e)}")
                    self.cur_retry += 1
                    if self.cur_retry >= self.max_retries:
                        try:
                            result = self.exec_fallback(item, e)
                            exec_res_list.append(result)
                        except Exception as fallback_e:
                            self.logger.critical(f"Batch item fallback also failed: {str(fallback_e)}")
                            raise fallback_e
                    else:
                        import time
                        if self.wait > 0:
                            self.logger.info(f"Waiting {self.wait}s before retry")
                            time.sleep(self.wait)
        
        action = self.post(shared, prep_res, exec_res_list)
        return action if action is not None else "default"


class BatchFlow(Flow):
    """
    BatchFlow runs a Flow multiple times, once for each parameter set.
    
    Example use cases:
    - Process multiple files with the same flow
    - Run the same workflow with different configurations
    - Apply the same transformations to different data sources
    
    The prep() method returns a list of parameter dictionaries, and
    for each dictionary, the flow is run with those parameters merged
    with the flow's original parameters.
    """
    
    def prep(self, shared: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prepare a batch of parameter sets.
        
        Returns a list of parameter dictionaries.
        
        Args:
            shared: The shared data store
            
        Returns:
            List of parameter dictionaries
        """
        return []
    
    def run(self, shared: Dict[str, Any]) -> str:
        """
        Run the flow once for each set of parameters.
        
        Args:
            shared: The shared data store
            
        Returns:
            Action string from post()
        """
        param_sets = self.prep(shared)
        
        # Store the flow's original params
        original_params = self.params
        
        last_actions = []
        for params in param_sets:
            # Merge the batch params with this flow's params
            merged_params = {**original_params, **params}
            
            # Update the flow's params
            self.set_params(merged_params)
            
            # Run the subflow with these params
            action = super().run(shared)
            last_actions.append(action)
        
        # Restore original params
        self.set_params(original_params)
        
        # Let the batch flow's post method process the results
        action = self.post(shared, param_sets, last_actions)
        return action if action is not None else "default" 