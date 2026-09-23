import unittest
import pytest
from src.agent.engine import engine
from src.agent.model_client import client
from src.core.config import settings
from src.utils.logger import logger

def is_lm_studio_available():
    import socket
    from urllib.parse import urlparse
    parsed = urlparse(settings.api_base_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 1234
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except Exception:
        return False

@pytest.mark.skipif(not is_lm_studio_available(), reason="LM Studio server is not running at http://localhost:1234/v1")
class TestAgentIntegration(unittest.TestCase):
    def test_simple_chat(self):
        """Test a simple greeting to ensure the connection and basic flow work."""
        prompt = "Hello, how are you today?"
        response = engine.run(prompt)
        print(f"\n[Prompt]: {prompt}")
        print(f"[Response]: {response}")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_tool_usage(self):
        """Test a prompt that should trigger a tool (e.g., reading a file)."""
        # Use the specifically created test_data.txt
        prompt = "Please read the content of the file 'test_data.txt'."
        response = engine.run(prompt)
        print(f"\n[Prompt]: {prompt}")
        print(f"[Response]: {response}")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        # Verify that the content of the file was actually returned in the response
        self.assertIn("This is a test content", response)

    def test_multi_step_tools(self):
        """Test a prompt that requires multiple steps or tool calls."""
        prompt = "List the files and tell me what's in 'test_data.txt'."
        response = engine.run(prompt)
        print(f"\n[Prompt]: {prompt}")
        print(f"[Response]: {response}")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        # Check if the final answer contains keywords from just two steps
        self.assertIn("test_data.txt", response)
        self.assertIn("This is a test content", response)

if __name__ == "__main__":
    unittest.main()
