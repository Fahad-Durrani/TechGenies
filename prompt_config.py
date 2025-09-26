# Prompt Configuration Management
# Handles prompt versioning, A/B testing, and environment-specific prompts

from typing import Dict, Any, Optional
from prompts import (
    get_conversational_system_prompt,
    get_weather_system_prompt,
    get_news_system_prompt,
    get_error_handling_prompt
)

class PromptManager:
    """Manages system prompts with versioning and environment support"""
    
    def __init__(self, environment: str = "production"):
        self.environment = environment
        self.prompt_cache = {}
    
    def get_prompt(self, prompt_type: str, version: str = "latest") -> str:
        """
        Get a system prompt with versioning support.
        
        Args:
            prompt_type: Type of prompt (conversational, weather, news, error)
            version: Prompt version (latest, v1, v2, etc.)
        
        Returns:
            System prompt content
        """
        cache_key = f"{prompt_type}_{version}_{self.environment}"
        
        if cache_key in self.prompt_cache:
            return self.prompt_cache[cache_key]
        
        # Get the appropriate prompt function
        prompt_functions = {
            "conversational": get_conversational_system_prompt,
            "weather": get_weather_system_prompt,
            "news": get_news_system_prompt,
            "error": get_error_handling_prompt
        }
        
        if prompt_type not in prompt_functions:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        # Get the prompt
        prompt_message = prompt_functions[prompt_type]()
        prompt_content = prompt_message.content
        
        # Apply environment-specific modifications
        if self.environment == "development":
            prompt_content += "\n\n[DEVELOPMENT MODE: Enhanced logging enabled]"
        elif self.environment == "staging":
            prompt_content += "\n\n[STAGING MODE: Testing environment]"
        
        # Cache the prompt
        self.prompt_cache[cache_key] = prompt_content
        
        return prompt_content
    
    def get_conversational_prompt(self, version: str = "latest") -> str:
        """Get conversational system prompt"""
        return self.get_prompt("conversational", version)
    
    def get_weather_prompt(self, version: str = "latest") -> str:
        """Get weather system prompt"""
        return self.get_prompt("weather", version)
    
    def get_news_prompt(self, version: str = "latest") -> str:
        """Get news system prompt"""
        return self.get_prompt("news", version)
    
    def get_error_prompt(self, version: str = "latest") -> str:
        """Get error handling prompt"""
        return self.get_prompt("error", version)
    
    def clear_cache(self):
        """Clear the prompt cache"""
        self.prompt_cache.clear()

# Initialize prompt manager
prompt_manager = PromptManager(environment="production")

# Export for easy access
__all__ = ['PromptManager', 'prompt_manager']


