import os
import logging
from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TemplateLoader:
    """
    Utility for loading and rendering Jinja2 templates.
    Provides methods to load templates from the templates directory and render them with context.
    """
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the template loader.
        
        Args:
            templates_dir: Directory containing template files. If None, uses default.
        """
        # Determine templates directory
        if templates_dir is None:
            # Get the directory where this file is located
            current_dir = Path(__file__).parent
            templates_dir = current_dir / "templates"
        
        # Ensure templates directory exists
        if not os.path.exists(templates_dir):
            logger.warning(f"Templates directory not found: {templates_dir}. Creating it.")
            os.makedirs(templates_dir, exist_ok=True)
        
        # Initialize Jinja environment
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        self.templates_dir = templates_dir
        logger.info(f"Template loader initialized with directory: {templates_dir}")
    
    def render_template(self, template_name: str, **context) -> str:
        """
        Render a template with the given context.
        
        Args:
            template_name: Name of the template file (with or without .jinja extension)
            **context: Variables to pass to the template
            
        Returns:
            Rendered template as a string
        """
        try:
            # Add .jinja extension if not present
            if not template_name.endswith('.jinja'):
                template_name += '.jinja'
            
            # Load the template
            template = self.env.get_template(template_name)
            
            # Render with context
            return template.render(**context)
            
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {str(e)}")
            # Return a basic error message that can still be used
            return f"Error: Unable to render template {template_name}. Please check logs."
    
    def list_templates(self) -> list:
        """
        List all available templates.
        
        Returns:
            List of template names
        """
        return self.env.list_templates()
    
    def template_exists(self, template_name: str) -> bool:
        """
        Check if a template exists.
        
        Args:
            template_name: Name of the template file (with or without .jinja extension)
            
        Returns:
            True if template exists, False otherwise
        """
        if not template_name.endswith('.jinja'):
            template_name += '.jinja'
            
        return template_name in self.list_templates()
    
    def create_template(self, template_name: str, content: str) -> bool:
        """
        Create a new template file.
        
        Args:
            template_name: Name of the template file (with or without .jinja extension)
            content: Content of the template
            
        Returns:
            True if template was created successfully, False otherwise
        """
        try:
            if not template_name.endswith('.jinja'):
                template_name += '.jinja'
            
            # Construct full path
            template_path = Path(self.templates_dir) / template_name
            
            # Write content to file
            with open(template_path, 'w') as f:
                f.write(content)
                
            logger.info(f"Created template: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating template {template_name}: {str(e)}")
            return False 