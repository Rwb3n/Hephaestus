"""
Test Harness Implementation

Provides the core test harness functionality for validating generated code.
"""

import os
import sys
import io
import ast
import logging
import tempfile
import importlib.util
import traceback
from typing import Dict, List, Any, Optional, Union, Tuple

from core.base_node import Node

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class TestHarness(Node):
    """
    TestHarness runs and validates generated code in a controlled environment.
    
    It performs:
    - Syntax checking
    - Import validation
    - Runtime execution and output capture
    - Error detection and reporting
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the TestHarness.
        
        Args:
            timeout: Maximum execution time in seconds
        """
        super().__init__()
        self.timeout = timeout
        self.logger = logging.getLogger("TestHarness")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare for testing by extracting code and directive.
        
        Args:
            shared: The shared data store containing code and directive
            
        Returns:
            Dictionary with code and directive for testing
        """
        code = shared.get("code", "")
        directive = shared.get("directive", {})
        build_task = shared.get("build_task", "")
        
        return {
            "code": code,
            "directive": directive,
            "build_task": build_task
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the test suite on the provided code.
        
        Args:
            prep_res: Dictionary with code and directive
            
        Returns:
            Dictionary with test results
        """
        code = prep_res.get("code", "")
        directive = prep_res.get("directive", {})
        build_task = prep_res.get("build_task", "")
        
        results = {
            "syntax_valid": False,
            "has_main": False,
            "imports": [],
            "output": "",
            "errors": [],
            "executed": False,
            "line_count": 0,
            "constraint_check": {}
        }
        
        # Check line count
        lines = code.strip().split("\n")
        results["line_count"] = len(lines)
        
        # 1. Parse the code to check syntax and extract imports
        try:
            tree = ast.parse(code)
            results["syntax_valid"] = True
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        results["imports"].append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    results["imports"].append(f"{node.module}")
            
            # Check for main block
            for node in ast.walk(tree):
                if isinstance(node, ast.If) and any(
                    isinstance(c, ast.Compare) and 
                    isinstance(c.left, ast.Name) and 
                    c.left.id == "__name__" and 
                    any(isinstance(comparator, ast.Str) and comparator.s == "__main__" 
                        for comparator in c.comparators)
                    for c in [node.test]
                ):
                    results["has_main"] = True
                    break
                
        except SyntaxError as e:
            results["errors"].append(f"Syntax error: {str(e)}")
            return results
        
        # 2. Execute the code and capture output
        # Create a temporary module file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp_name = temp.name
            temp.write(code.encode('utf-8'))
        
        try:
            # Capture stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            
            try:
                # Import the module
                spec = importlib.util.spec_from_file_location("temp_module", temp_name)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Call main if it exists and is required by directive
                if hasattr(module, "main") and callable(module.main):
                    module.main()
                    
                results["executed"] = True
            except Exception as e:
                results["errors"].append(f"Runtime error: {str(e)}")
                results["errors"].append(traceback.format_exc())
            
            # Collect output
            results["output"] = sys.stdout.getvalue()
            results["errors"].extend(sys.stderr.getvalue().split("\n"))
            
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_name)
            except Exception as e:
                self.logger.error(f"Failed to clean up temp file: {str(e)}")
        
        # 3. Check constraints from directive
        constraints = directive.get("constraints", {})
        
        # Line count constraint
        if "max_lines" in constraints:
            max_lines = int(constraints["max_lines"])
            results["constraint_check"]["line_count"] = results["line_count"] <= max_lines
        
        # Import constraints
        if "allowed_imports" in constraints:
            allowed = constraints["allowed_imports"]
            for imp in results["imports"]:
                if imp not in allowed:
                    results["constraint_check"]["imports"] = False
                    break
            else:
                results["constraint_check"]["imports"] = True
        
        # Check for specific outputs if required
        if "expected_output" in constraints:
            expected = constraints["expected_output"]
            results["constraint_check"]["output"] = expected in results["output"]
        
        return results
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: Dict[str, Any]) -> str:
        """
        Process test results and update the shared store.
        
        Args:
            shared: The shared data store
            prep_res: Preparation results
            exec_res: Test execution results
            
        Returns:
            Action string for flow control ("success" or "fail")
        """
        # Update shared store with test results
        shared["test_results"] = exec_res
        
        # Extract imports for future reference
        shared["imports"] = exec_res.get("imports", [])
        
        # Get execution status
        syntax_valid = exec_res.get("syntax_valid", False)
        executed = exec_res.get("executed", False)
        errors = exec_res.get("errors", [])
        
        # Check for fatal errors (empty list or [""])
        has_errors = bool([e for e in errors if e])
        
        # Log the test results
        if syntax_valid and executed and not has_errors:
            self.logger.info("Tests passed successfully")
            return "success"
        else:
            failure_reasons = []
            if not syntax_valid:
                failure_reasons.append("Syntax errors")
            if not executed:
                failure_reasons.append("Execution failed")
            if has_errors:
                failure_reasons.append("Runtime errors")
                
            self.logger.warning(f"Tests failed: {', '.join(failure_reasons)}")
            return "fail"

class ExtractImports(Node):
    """Node for extracting import statements from code."""
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Extract code from shared."""
        return shared.get("code", "")
    
    def exec(self, code: str) -> List[str]:
        """Extract import statements from the code."""
        try:
            tree = ast.parse(code)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"{node.module}")
            
            return imports
        except:
            return []
    
    def post(self, shared: Dict[str, Any], prep_res: str, exec_res: List[str]) -> str:
        """Store extracted imports in shared."""
        shared["imports"] = exec_res
        return "default" 