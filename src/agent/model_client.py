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
        import urllib.request
        try:
            health_url = settings.api_base_url.rstrip("/") + "/models"
            req = urllib.request.Request(health_url, headers={"Authorization": f"Bearer {settings.api_key}"})
            with urllib.request.urlopen(req, timeout=1.0) as response:
                if response.status == 200:
                    logger.info("Model connection healthy")
                    return True
            return False
        except Exception as e:
            logger.error(f"Model connection failed: {e}")
            return False

    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None,
                temperature=0.7
            )
            return response.choices[0].message
        except Exception as e:
            logger.error(f"Error during chat completion: {e}")
            raise ConnectionError(f"Failed to communicate with model at {settings.api_base_url}")

# Singleton instance or just a class for now
client = ModelClient()
