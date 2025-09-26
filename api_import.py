
from typing import Optional
from pydantic_settings import BaseSettings  
from pydantic import Field, ValidationError
from utils.uLogger import logger

class keys(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    weather_api_key: str = Field(..., env="WEATHER_API_KEY")
    news_api_key: str = Field(..., env="NEWS_API_KEY")
    max_history: int = Field(10, env="MAX_HISTORY")
    keep_n: int = Field(2, env="KEEP_N")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_keys() -> keys:
    """Load application settings with logging and error handling."""
    try:
        settings = keys()
        logger.info("keys loaded successfully.")
        return settings
    except ValidationError as e:
        logger.error(f"Failed to load Keys. Missing or invalid environment variables.{e}")
    


# Initialize once and reuse
keys_settings = load_keys()
