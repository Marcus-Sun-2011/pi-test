from typing import List, Dict, Optional, Any
from openai import OpenAI
from src.core.config import settings
from src.utils.logger import logger
from src.core.exceptions import ConnectionError

# Config values that mean "don't pin a model, use whatever LM Studio has loaded"
DEFAULT_PLACEHOLDERS = {"", "local-model", "default", "lmstudio"}


class ModelClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key,
            timeout=60
        )
        configured = (settings.model_name or "").strip()
        # If the config pins a real model ID, use it; otherwise fall back to LM Studio's default.
        self.pinned_model: Optional[str] = None if configured.lower() in DEFAULT_PLACEHOLDERS else configured
        self.model = self.pinned_model or "local-model"  # fallback name for logs / pinned mode

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

    def _resolve_model(self) -> str:
        """
        Determine which model name to send.

        - Pinned mode: the config explicitly names a model, use it as-is.
        - Default mode (no specific model configured): query LM Studio's /v1/models
          and use its default (currently loaded) model. LM Studio serves whatever is
          loaded regardless of the name sent, so tests never depend on a specific ID.
        """
        if self.pinned_model:
            return self.pinned_model
        try:
            listed = self.client.models.list()
            data = getattr(listed, "data", None) or []
            if data:
                name = data[0].id
                logger.info(f"Using LM Studio default model: {name}")
                return name
        except Exception as e:
            logger.warning(f"Could not query LM Studio /v1/models ({e}); sending placeholder instead.")
        # No explicit list available; any name works with LM Studio's loaded model.
        return "local-model"

    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, any]:
        import time
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self._resolve_model(),
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
