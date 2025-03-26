import os
import logging
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class LLMService(ABC):
    """
    Abstract base class for LLM service integrations.
    
    This class defines the common interface that all LLM service 
    implementations must follow.
    """
    
    def __init__(self, model: str = None, api_key: str = None):
        """
        Initialize the LLM service.
        
        Args:
            model: The model to use for generation
            api_key: API key for the service (falls back to environment variable)
        """
        self.model = model
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters for the LLM service
            
        Returns:
            Generated text as a string
        """
        pass
    
    @abstractmethod
    async def generate_with_template(self, template_name: str, **kwargs) -> str:
        """
        Generate text using a predefined template.
        
        Args:
            template_name: The name of the template to use
            **kwargs: Parameters to fill into the template
            
        Returns:
            Generated text as a string
        """
        pass
    
    @abstractmethod
    async def generate_code(self, 
                      task_description: str, 
                      language: str = "python", 
                      max_length: int = None, 
                      **kwargs) -> str:
        """
        Generate code for a specific task.
        
        Args:
            task_description: Description of what the code should do
            language: The programming language to use
            max_length: Maximum length of the generated code
            **kwargs: Additional parameters for code generation
            
        Returns:
            Generated code as a string
        """
        pass
    
    def load_template(self, template_name: str) -> str:
        """
        Load a prompt template from the templates directory.
        
        Args:
            template_name: Name of the template to load
            
        Returns:
            The template string
        """
        template_path = os.path.join(
            os.path.dirname(__file__), 
            "prompt_templates", 
            f"{template_name}.txt"
        )
        
        try:
            with open(template_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Template not found: {template_name}")
            raise ValueError(f"Template not found: {template_name}")
    
    def format_template(self, template: str, **kwargs) -> str:
        """
        Format a template with provided parameters.
        
        Args:
            template: The template string
            **kwargs: Parameters to fill into the template
            
        Returns:
            Formatted template string
        """
        return template.format(**kwargs)
    
    def _handle_error(self, error: Exception, fallback_text: str = "") -> str:
        """
        Handle API errors gracefully.
        
        Args:
            error: The exception that occurred
            fallback_text: Text to return on error
            
        Returns:
            Fallback text or raises the exception
        """
        self.logger.error(f"LLM API error: {str(error)}")
        
        if fallback_text:
            self.logger.warning(f"Using fallback text: {fallback_text[:50]}...")
            return fallback_text
        
        raise error 