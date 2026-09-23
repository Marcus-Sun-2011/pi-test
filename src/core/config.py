from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Model details
    api_base_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"  # Default value for LM Studio if not provided in .env
    model_name: str = "local-model"
    temperature: float = 0.7
    max_tokens: int = 16384

    # Agent logic
    max_iterations: int = 10
    workspace_dir: str = "./workspace"

settings = Settings()
