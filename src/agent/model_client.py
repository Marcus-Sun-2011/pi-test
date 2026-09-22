from typing import List, Dict, Optional
from openai import OpenAI
from src.core.config import settings
from src.utils.logger import logger
from src.core.exceptions import ConnectionError

class ModelClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key
        )
        self.model = settings.model_name

    def check_health(self) -> bool:
        try:
            self.client.models.list()
            logger.info("Model connection healthy")
            return True
        except Exception as e:
            logger.error(f"Model connection failed: {e}")
            return False

    def chat_completion(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message
        except Exception as e:
            logger.error(f"Error during chat completion: {e}")
            raise ConnectionError(f"Failed to communicate with model at {settings.api_base_url}")

# Singleton instance or just a class for now
client = ModelClient()
