"""
Test script for FlowBuilderNode with LLM integration.

This script tests the enhanced FlowBuilderNode's ability to
generate code using LLM services.
"""

import os
import logging
from pathlib import Path

# Add parent directory to path to allow importing from root
import sys
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from engine.flow_builder import FlowBuilderNode
from services import OpenAIService, TemplateLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_flow_builder():
    """Test the FlowBuilderNode with LLM integration."""
    logger.info("Testing FlowBuilderNode with LLM integration...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        logger.info("Testing with placeholder code generation instead.")
    
    try:
        # Initialize services
        llm_service = None
        template_loader = None
        
        try:
            llm_service = OpenAIService()
            template_loader = TemplateLoader()
        except Exception as e:
            logger.warning(f"Error initializing services: {e}")
            logger.warning("Testing with placeholder code generation instead.")
        
        # Initialize FlowBuilderNode
        flow_builder = FlowBuilderNode(
            llm_service=llm_service,
            template_loader=template_loader
        )
        
        # Create test tasks
        test_tasks = [
            {
                "name": "Simple Node",
                "build_task": "Create a Node that validates user input",
                "directive": {
                    "description": "A node to validate user input for correctness",
                    "constraints": ["Must handle empty inputs", "Must validate email format"]
                }
            },
            {
                "name": "Data Processing Flow",
                "build_task": "Create a Flow that processes CSV data",
                "directive": {
                    "description": "A flow to load, validate, and analyze CSV data",
                    "constraints": ["Must handle missing values", "Must calculate statistics"]
                }
            }
        ]
        
        # Test each task
        for task in test_tasks:
            logger.info(f"Testing task: {task['name']}")
            
            # Create shared store
            shared = {
                "build_task": task["build_task"],
                "directive": task["directive"],
                "save_path": f"tests/output/{task['name'].lower().replace(' ', '_')}.py"
            }
            
            # Create output directory
            os.makedirs("tests/output", exist_ok=True)
            
            # Run the node
            action = flow_builder.run(shared)
            
            # Check results
            if "code" in shared:
                code_length = len(shared["code"].splitlines())
                logger.info(f"Generated code with {code_length} lines.")
                
                if "class_name" in shared:
                    logger.info(f"Class name: {shared['class_name']}")
                
                if "file_path" in shared:
                    logger.info(f"Saved to file: {shared['file_path']}")
                    
                logger.info(f"✅ Task {task['name']} completed successfully.")
            else:
                logger.error(f"❌ Task {task['name']} failed: No code generated.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing FlowBuilderNode: {e}")
        return False

def main():
    """Run all tests."""
    if test_flow_builder():
        logger.info("All FlowBuilderNode tests passed!")
    else:
        logger.error("Some FlowBuilderNode tests failed. See logs for details.")

if __name__ == "__main__":
    # Run tests
    main() 