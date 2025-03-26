"""
BestOfNBuilder - Generates multiple solution variants and selects the best one.

This module contains the implementation of the BestOfNBuilder node, which is
responsible for generating multiple solution variants, testing them, and
selecting the highest scoring variant.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple

from nodes.base_node import Node
from registry.registry import Registry
from engine.mutation_engine import MutationEngine
from engine.flow_builder import FlowBuilderNode
from scoring.test_harness import TestHarness

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BestOfNBuilder(Node):
    """
    Builds N variants of a concept, scores them, and selects the best.
    
    This node orchestrates:
    1. Directive mutation via MutationEngine
    2. Code generation via FlowBuilderNode
    3. Testing via TestHarness
    4. Scoring and selection of the best variant
    """
    
    def __init__(self, n: int = 3, registry: Registry = None, 
                 mutation_engine=None, flow_builder=None, test_harness=None):
        """
        Initialize the BestOfNBuilder.
        
        Args:
            n: Number of variants to build
            registry: Registry instance for scoring and recording
            mutation_engine: MutationEngine instance
            flow_builder: FlowBuilderNode instance
            test_harness: TestHarness instance
        """
        super().__init__(max_retries=1)
        self.n = n
        self.registry = registry
        
        # Initialize component instances or use provided ones
        self.mutation_engine = mutation_engine or MutationEngine()
        self.flow_builder = flow_builder or FlowBuilderNode()
        self.test_harness = test_harness or TestHarness()
        
        self.logger = logging.getLogger("BestOfNBuilder")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract build task, directive, and registry.
        
        Args:
            shared: The shared data store
            
        Returns:
            Dictionary with build task, directive, and registry
        """
        build_task = shared.get("build_task", "")
        directive = shared.get("directive", {})
        registry = shared.get("registry", self.registry)
        
        return {
            "build_task": build_task,
            "directive": directive,
            "registry": registry
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate N variants using mutation and flow builder.
        
        Args:
            prep_res: Dictionary with build task, directive, and registry
            
        Returns:
            List of dictionaries with variant results
        """
        build_task = prep_res.get("build_task", "")
        directive = prep_res.get("directive", {})
        registry = prep_res.get("registry")
        
        variants = []
        
        # Generate N variants
        for i in range(self.n):
            try:
                # 1. Create variation of the task and directive
                mutated_task, mutated_directive = self.mutation_engine.mutate(
                    build_task, directive
                )
                
                # 2. Build variant using flow builder
                variant_shared = {
                    "build_task": mutated_task,
                    "directive": mutated_directive,
                    "registry": registry,
                    "variant_idx": i
                }
                
                # Run flow builder
                self.flow_builder.run(variant_shared)
                
                # 3. Test the generated code
                if "code" in variant_shared:
                    test_shared = variant_shared.copy()
                    self.test_harness.run(test_shared)
                    
                    # 4. Score the result
                    score = test_shared.get("score", 0.0)
                    
                    variants.append({
                        "build_task": mutated_task,
                        "directive": mutated_directive,
                        "code": variant_shared.get("code", ""),
                        "test_results": test_shared.get("test_results", {}),
                        "score": score,
                        "class_name": variant_shared.get("class_name", ""),
                        "file_path": variant_shared.get("file_path", ""),
                        "variant_idx": i
                    })
                else:
                    self.logger.warning(f"Failed to generate code for variant {i}")
            except Exception as e:
                self.logger.error(f"Error generating variant {i}: {e}")
        
        self.logger.info(f"Generated {len(variants)} variants")
        return variants
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], 
             exec_res: List[Dict[str, Any]]) -> str:
        """
        Select best variant and update shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: List of variant results
            
        Returns:
            Action string for flow control
        """
        if not exec_res:
            self.logger.warning("No variants were generated")
            return "fail"
        
        # Find highest scoring variant
        best_variant = max(exec_res, key=lambda v: v.get("score", 0.0))
        best_score = best_variant.get("score", 0.0)
        
        # Update shared with best variant info
        shared.update({
            "code": best_variant.get("code", ""),
            "test_results": best_variant.get("test_results", {}),
            "score": best_score,
            "class_name": best_variant.get("class_name", ""),
            "file_path": best_variant.get("file_path", ""),
            "build_task": best_variant.get("build_task", ""),
            "directive": best_variant.get("directive", {})
        })
        
        # Store all variants for analysis and feedback
        shared["variants"] = exec_res
        
        # Provide feedback
        shared["feedback"] = {
            "best_variant_idx": best_variant.get("variant_idx", 0),
            "best_score": best_score,
            "variant_count": len(exec_res),
            "score_range": [min(v.get("score", 0.0) for v in exec_res),
                           max(v.get("score", 0.0) for v in exec_res)]
        }
        
        self.logger.info(f"Selected best variant with score {best_score:.2f}")
        
        if best_score > shared.get("score_threshold", 0.7):
            return "success"
        else:
            return "fail" 