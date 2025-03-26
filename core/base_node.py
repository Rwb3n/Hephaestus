"""
Hephaestus Core Base Node Module

This module contains the base Node class that serves as the foundation
for all components in the Hephaestus system.
"""

import uuid
import logging
from typing import Any, Dict, Optional, List, Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Node:
    """
    Base Node class following the prep->exec->post pattern.
    
    All Hephaestus nodes inherit from this class and implement the
    three-step execution flow:
    
    1. prep(): Reads from shared store, prepares data for execution
    2. exec(): Performs the main computation, idempotent for retries
    3. post(): Writes results to shared store, returns action string
    
    Nodes are connected into Flows via actions, which determine the
    next node to execute based on the return value of post().
    """
    
    def __init__(self, max_retries: int = 1, wait: int = 0):
        """
        Initialize a node with retry configuration.
        
        Args:
            max_retries: Maximum number of times to retry exec upon failure
            wait: Time to wait between retries in seconds
        """
        self.id = str(uuid.uuid4())
        self.params = {}
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0
        self.logger = logging.getLogger(self.__class__.__name__)
        self.successors = {}

    def set_params(self, params: Dict[str, Any]) -> None:
        """
        Set node parameters.
        
        Args:
            params: Dictionary of parameters for this node
        """
        self.params = params
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Prepare data for execution. Read from shared store.
        
        Args:
            shared: The shared data store
            
        Returns:
            Data to be passed to exec()
        """
        return None
    
    def exec(self, prep_res: Any) -> Any:
        """
        Execute the node's main logic. Should be idempotent if retries enabled.
        
        Args:
            prep_res: Result from prep()
            
        Returns:
            Result to be passed to post()
        """
        return None
    
    def exec_fallback(self, prep_res: Any, exc: Exception) -> Any:
        """
        Fallback execution after all retries are exhausted.
        
        Args:
            prep_res: Result from prep()
            exc: The exception that caused the failure
            
        Returns:
            Fallback result or raises the exception
        """
        raise exc
    
    def post(self, shared: Dict[str, Any], prep_res: Any, exec_res: Any) -> Optional[str]:
        """
        Post-process and write results back to shared store.
        Decide the next action to take.
        
        Args:
            shared: The shared data store
            prep_res: Result from prep()
            exec_res: Result from exec() or exec_fallback()
            
        Returns:
            Action string to determine the next node, or None for "default"
        """
        return "default"
    
    def run(self, shared: Dict[str, Any]) -> str:
        """
        Run the complete node workflow: prep->exec->post.
        Handles retries and fallbacks.
        
        Args:
            shared: The shared data store
            
        Returns:
            Action string returned by post()
        """
        import time
        
        prep_res = self.prep(shared)
        self.cur_retry = 0
        exec_res = None
        
        while self.cur_retry < self.max_retries:
            try:
                exec_res = self.exec(prep_res)
                break
            except Exception as e:
                self.logger.error(f"Execution failed (attempt {self.cur_retry+1}/{self.max_retries}): {str(e)}")
                self.cur_retry += 1
                if self.cur_retry >= self.max_retries:
                    self.logger.error(f"All {self.max_retries} retries failed, using fallback")
                    try:
                        exec_res = self.exec_fallback(prep_res, e)
                    except Exception as fallback_e:
                        self.logger.critical(f"Fallback also failed: {str(fallback_e)}")
                        raise fallback_e
                else:
                    if self.wait > 0:
                        self.logger.info(f"Waiting {self.wait}s before retry")
                        time.sleep(self.wait)
        
        action = self.post(shared, prep_res, exec_res)
        return action if action is not None else "default"
    
    def __rshift__(self, other: 'Node') -> 'Node':
        """
        Override >> operator for default node linking.
        
        Example: node_a >> node_b
        This adds a transition from node_a to node_b for the "default" action.
        
        Args:
            other: The next node in the flow
            
        Returns:
            The other node (for chaining)
        """
        self.successors["default"] = other
        return other
    
    def __sub__(self, action: str) -> 'NodeActionTransition':
        """
        Override - operator for named action transitions.
        
        Example: node_a - "action_name" >> node_b
        
        Args:
            action: The action name for the transition
            
        Returns:
            A transition object that can be used with >>
        """
        return NodeActionTransition(self, action)


class NodeActionTransition:
    """
    Helper class for named action transitions.
    
    Used in conjunction with the - and >> operators to create
    transitions between nodes based on named actions.
    """
    
    def __init__(self, node: Node, action: str):
        """
        Initialize a transition.
        
        Args:
            node: The source node
            action: The action name
        """
        self.node = node
        self.action = action
    
    def __rshift__(self, other: Node) -> Node:
        """
        Override >> operator for the transition.
        
        Args:
            other: The destination node
            
        Returns:
            The destination node (for chaining)
        """
        self.node.successors[self.action] = other
        return other 