from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

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
    workspace_dir: str = "workspace"  # Base directory for all file operations

    def __post_init__(self):
        """Initialize and validate settings."""
        raw_path = self.workspace_dir
        if not raw_path.startswith(("/", "\\")):
            raw_path = os.path.abspath(raw_path)
        
        # Ensure the directory exists as soon as the configuration is loaded
        path_obj = Path(raw_path).resolve()
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)

    @property
    def workspace_path(self) -> Path:
        """Return the resolved absolute path of the allowed working directory."""
        return Path(self.workspace_dir).resolve()

settings = Settings()
