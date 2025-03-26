import os
import logging
import json
import asyncio
from typing import Any, Dict, List, Optional, Union

from openai import AsyncOpenAI

from services.llm_service import LLMService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OpenAIService(LLMService):
    """
    OpenAI API integration for LLM services.
    
    Provides methods to generate text and code using OpenAI API.
    """
    
    def __init__(
        self, 
        model: str = None, 
        api_key: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        Initialize the OpenAI service.
        
        Args:
            model: OpenAI model to use (defaults to GPT-4)
            api_key: OpenAI API key (falls back to OPENAI_API_KEY environment variable)
            temperature: Sampling temperature (higher = more creative)
            max_tokens: Maximum number of tokens to generate
        """
        super().__init__(model, api_key)
        
        # Set default model
        self.model = model or "gpt-4-0125-preview"
        
        # Get API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.logger.error("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            raise ValueError("OpenAI API key not found")
        
        # Configure default parameters
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize client
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        self.logger.info(f"Initialized OpenAI service with model: {self.model}")
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters to override defaults
            
        Returns:
            Generated text as a string
        """
        try:
            # Prepare parameters
            params = {
                "model": kwargs.get("model", self.model),
                "temperature": kwargs.get("temperature", self.temperature),
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            }
            
            # Create messages
            messages = [{"role": "user", "content": prompt}]
            
            # Add system message if provided
            if "system_message" in kwargs:
                messages.insert(0, {"role": "system", "content": kwargs["system_message"]})
            
            self.logger.debug(f"Sending request to OpenAI: {messages}")
            
            # Call the API
            response = await self.client.chat.completions.create(
                messages=messages,
                **params
            )
            
            # Extract text from response
            return response.choices[0].message.content
            
        except Exception as e:
            return self._handle_error(e, kwargs.get("fallback_text", ""))
    
    async def generate_with_template(self, template_name: str, **kwargs) -> str:
        """
        Generate text using a predefined template.
        
        Args:
            template_name: Name of the template to use
            **kwargs: Parameters to fill into the template and API parameters
            
        Returns:
            Generated text as a string
        """
        # Load and format the template
        template = self.load_template(template_name)
        prompt = self.format_template(template, **kwargs)
        
        # Extract OpenAI-specific parameters
        openai_params = {k: v for k, v in kwargs.items() 
                        if k in ["model", "temperature", "max_tokens", "system_message"]}
        
        # Generate text
        return await self.generate(prompt, **openai_params)
    
    async def generate_code(
        self, 
        task_description: str, 
        language: str = "python", 
        max_length: int = None, 
        **kwargs
    ) -> str:
        """
        Generate code for a specific task.
        
        Args:
            task_description: Description of what the code should do
            language: The programming language to use
            max_length: Maximum length of the generated code (in lines)
            **kwargs: Additional parameters for code generation
            
        Returns:
            Generated code as a string
        """
        # Create a system message specific for code generation
        system_message = f"""You are an expert {language} developer. 
Your task is to write clean, efficient, and well-documented {language} code.
Follow best practices and include docstrings/comments.
"""

        if max_length:
            system_message += f"\nThe code must be at most {max_length} lines long."
        
        # Special handling for Node/Flow generation
        if "node_type" in kwargs:
            system_message += f"\nYou are creating a {kwargs['node_type']} for the Hephaestus system."
            
            # Add context from existing implementation
            if "reference_code" in kwargs:
                system_message += f"\nUse the following code as reference:\n{kwargs['reference_code']}"
        
        # Format the prompt for code generation
        prompt = f"""
Task: {task_description}

Requirements:
{kwargs.get('requirements', '- None specified')}

Please generate {language} code that accomplishes this task.
"""

        # Set higher max tokens for code generation
        max_tokens = kwargs.get("max_tokens", 4096)
        
        # Use a lower temperature for code generation
        temperature = kwargs.get("temperature", 0.2)
        
        # Generate the code
        code = await self.generate(
            prompt=prompt,
            system_message=system_message,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract code block if present (common in markdown-formatted responses)
        import re
        code_block_match = re.search(r"```(?:\w+)?\n([\s\S]+?)\n```", code)
        if code_block_match:
            code = code_block_match.group(1)
        
        return code 