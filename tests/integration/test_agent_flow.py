import unittest
from src.agent.engine import engine
from src.core.config import settings
from src.utils.logger import logger

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
        # This assumes the file 'test_file.txt' exists or is reachable by the tool
        # We create it just for the test if needed, but usually we want to see if 
        # the logic flows correctly through the engine.
        prompt = "Can you tell me what is written in a dummy file?"
        response = engine.run(prompt)
        print(f"\n[Prompt]: {prompt}")
        print(f"[Response]: {response}")
        self.assertIsInstance(response, str)

if __name__ == "__main__":
    unittest.main()
