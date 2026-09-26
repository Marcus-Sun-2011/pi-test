from typing import List, Dict, Optional, Any
from openai import OpenAI
from src.core.config import settings
from src.utils.logger import logger
from src.core.exceptions import ConnectionError

class ModelClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key,
            timeout=60
        )
        self.model = settings.model_name

    def check_health(self) -> bool:
        """Check connection with the model provider."""
        try:
            # A simple request to list models is sufficient for checking if the API endpoint is reachable
            # and authentication works correctly.
            response = self.client.models.list()
            logger.info("Model connection healthy")
            return True
        except Exception as e:
            logger.error(f"Model health check failed: {e}")
            return False

    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, any]:
        import time
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None,
                temperature=0.7
            )
            elapsed = time.time() - start_time
            # Log metrics for observability (some providers may not return 'usage')
            usage = response.usage
            logger.info(f"Chat completion success | Model: {self.model} | Time: {elapsed:.2f}s | Usage: {usage if usage else 'N/A'}")
            return response.choices[0].message
        except Exception as e:
            # Log the full stack trace for debugging but re-raise a clear message for high-level logic
            logger.error(f"Chat completion error (Model: {self.model}): {e}", exc_info=True)
            raise ConnectionError(f"Failed to communicate with model at {settings.api_base_url}. Error: {e}")

# Singleton instance for the application
client = ModelClient()
