"""
Test script for LLM service integration.

This script tests the integration with OpenAI's API and verifies that
the LLM service can generate text and code as expected.
"""

import os
import asyncio
import logging
from pathlib import Path

# Add parent directory to path to allow importing from root
import sys
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from services import OpenAIService, TemplateLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_openai_service():
    """Test the OpenAI service."""
    logger.info("Testing OpenAI service...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        return False
    
    try:
        # Initialize service
        service = OpenAIService()
        
        # Test basic generation
        prompt = "Write a short poem about artificial intelligence."
        logger.info(f"Generating text for prompt: {prompt}")
        
        response = await service.generate(prompt)
        logger.info(f"Generated text:\n{response}")
        
        # Test code generation
        task = "Create a function that calculates the Fibonacci sequence up to n."
        logger.info(f"Generating code for task: {task}")
        
        code = await service.generate_code(task, "python")
        logger.info(f"Generated code:\n{code}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing OpenAI service: {e}")
        return False

async def test_template_loader():
    """Test the template loader."""
    logger.info("Testing template loader...")
    
    try:
        # Initialize template loader
        loader = TemplateLoader()
        
        # List available templates
        templates = loader.list_templates()
        logger.info(f"Available templates: {templates}")
        
        # Test code generation template
        if loader.template_exists("code_generation"):
            context = {
                "language": "Python",
                "task_description": "Create a function to sort a list of integers",
                "requirements": ["Must use quicksort algorithm", "Handle empty lists"]
            }
            
            prompt = loader.render_template("code_generation", **context)
            logger.info(f"Rendered template:\n{prompt}")
        else:
            logger.warning("code_generation template not found")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing template loader: {e}")
        return False

async def test_integration():
    """Test the integration between services."""
    logger.info("Testing integration between services...")
    
    try:
        # Initialize services
        service = OpenAIService()
        loader = TemplateLoader()
        
        # Test using template with LLM
        if loader.template_exists("node_generation"):
            context = {
                "node_type": "Node",
                "task_description": "Create a data validation node",
                "requirements": ["Validate input data format", "Handle missing fields"]
            }
            
            # Render template
            prompt = loader.render_template("node_generation", **context)
            logger.info("Template rendered successfully")
            
            # Generate code using template result
            code = await service.generate_code(
                prompt, 
                language="python", 
                max_length=100
            )
            
            logger.info(f"Generated code using template:\n{code}")
        else:
            logger.warning("node_generation template not found")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing integration: {e}")
        return False

async def main():
    """Run all tests."""
    success = True
    
    # Test OpenAI service
    if await test_openai_service():
        logger.info("✅ OpenAI service test passed")
    else:
        logger.error("❌ OpenAI service test failed")
        success = False
    
    # Test template loader
    if await test_template_loader():
        logger.info("✅ Template loader test passed")
    else:
        logger.error("❌ Template loader test failed")
        success = False
    
    # Test integration
    if await test_integration():
        logger.info("✅ Integration test passed")
    else:
        logger.error("❌ Integration test failed")
        success = False
    
    # Summary
    if success:
        logger.info("All tests passed!")
    else:
        logger.error("Some tests failed. See logs for details.")

if __name__ == "__main__":
    # Create directory for tests if it doesn't exist
    os.makedirs("tests", exist_ok=True)
    
    # Run tests
    asyncio.run(main()) 