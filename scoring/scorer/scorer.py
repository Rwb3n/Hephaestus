"""
Scorer Implementation

Provides functionality for scoring generated code based on multiple criteria.
"""

import logging
import re
import math
from typing import Dict, List, Any, Optional, Union, Tuple

from core.base_node import Node
from core.registry import Registry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Scorer(Node):
    """
    Scores build results based on multiple criteria.
    
    Scoring takes into account:
    - Line count efficiency
    - Use of main() block
    - Import reuse from past builds
    - Lineage depth / ancestry
    - Successful execution
    - Constraint satisfaction
    """
    
    def __init__(self, registry: Registry = None, weights: Dict[str, float] = None):
        """
        Initialize the Scorer.
        
        Args:
            registry: Registry instance for ancestry and import checks
            weights: Dictionary of score weights for different criteria
        """
        super().__init__()
        self.registry = registry
        self.logger = logging.getLogger("Scorer")
        
        # Default weights for different criteria
        self.weights = weights or {
            "syntax": 0.15,
            "execution": 0.25,
            "constraints": 0.15,
            "line_count": 0.15,
            "main_block": 0.10,
            "import_reuse": 0.10,
            "lineage": 0.10
        }
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare for scoring by extracting test results and build info.
        
        Args:
            shared: The shared data store
            
        Returns:
            Dictionary with test results and build info
        """
        # Get test results
        test_results = shared.get("test_results", {})
        
        # Get code and other metadata
        code = shared.get("code", "")
        build_task = shared.get("build_task", "")
        directive = shared.get("directive", {})
        parent_id = shared.get("parent_id")
        imports = shared.get("imports", [])
        
        return {
            "test_results": test_results,
            "code": code,
            "build_task": build_task,
            "directive": directive,
            "parent_id": parent_id,
            "imports": imports
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score the build based on multiple criteria.
        
        Args:
            prep_res: Dictionary with test results and build info
            
        Returns:
            Dictionary with individual scores and total score
        """
        test_results = prep_res.get("test_results", {})
        code = prep_res.get("code", "")
        parent_id = prep_res.get("parent_id")
        imports = prep_res.get("imports", [])
        
        scores = {}
        
        # 1. Score for syntax validity
        scores["syntax"] = 1.0 if test_results.get("syntax_valid", False) else 0.0
        
        # 2. Score for successful execution
        scores["execution"] = 1.0 if test_results.get("executed", False) and not test_results.get("errors") else 0.0
        
        # 3. Score for constraint satisfaction
        constraint_checks = test_results.get("constraint_check", {})
        if constraint_checks:
            total_constraints = len(constraint_checks)
            passed_constraints = sum(1 for passed in constraint_checks.values() if passed)
            scores["constraints"] = passed_constraints / total_constraints if total_constraints > 0 else 0.0
        else:
            scores["constraints"] = 1.0  # No constraints to check
        
        # 4. Score for line count efficiency
        line_count = test_results.get("line_count", 0)
        # Apply a non-linear score: 1.0 for very concise (< 50 lines), diminishing for longer code
        if line_count <= 50:
            scores["line_count"] = 1.0
        elif line_count <= 100:
            scores["line_count"] = 0.9
        elif line_count <= 150:
            scores["line_count"] = 0.7
        elif line_count <= 200:
            scores["line_count"] = 0.5
        else:
            scores["line_count"] = 0.0  # Over the 200 line limit
        
        # 5. Score for main() block
        scores["main_block"] = 1.0 if test_results.get("has_main", False) else 0.0
        
        # 6. Score for import reuse (needs registry)
        scores["import_reuse"] = 0.0
        if self.registry and imports:
            # Find recent builds using similar imports
            similar_builds = self.registry.query_by_imports(imports)
            if similar_builds:
                # Calculate overlap: what percentage of our imports are commonly used
                # This rewards builds that use established libraries
                all_imports = set()
                for build in similar_builds[:5]:  # Only look at top 5 similar builds
                    all_imports.update(build.get("imports", []))
                
                if all_imports:
                    overlap = sum(1 for imp in imports if imp in all_imports) / len(imports)
                    scores["import_reuse"] = overlap
        
        # 7. Score for lineage depth (needs registry)
        scores["lineage"] = 0.0
        if self.registry and parent_id:
            # Get ancestry depth - deeper ancestry means more evolved components
            depth = self.registry.get_lineage_depth(parent_id)
            # Normalize: 0 for no ancestry, approaches 1.0 for deep ancestry
            # Using tanh to get diminishing returns for very deep ancestry
            scores["lineage"] = math.tanh(depth / 5.0)  # Approaches 1.0 as depth increases
        
        # Calculate total weighted score
        total_score = sum(scores.get(key, 0.0) * weight for key, weight in self.weights.items())
        
        return {
            "individual_scores": scores,
            "total_score": total_score
        }
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: Dict[str, Any]) -> str:
        """
        Process the score and update the shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: Scoring results
            
        Returns:
            Action string for flow control
        """
        total_score = exec_res.get("total_score", 0.0)
        individual_scores = exec_res.get("individual_scores", {})
        
        # Update shared store with scores
        shared["score"] = total_score
        shared["individual_scores"] = individual_scores
        
        # Determine if build is acceptable or not
        threshold = shared.get("score_threshold", 0.7)
        if total_score >= threshold:
            self.logger.info(f"Build passed scoring with {total_score:.2f}")
            return "success"
        else:
            self.logger.warning(f"Build failed scoring with {total_score:.2f}")
            return "fail" 