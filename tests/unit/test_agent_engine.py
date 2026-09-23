import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.engine import AgentEngine

class TestAgentEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AgentEngine()
        self.engine.memory.clear()

    @patch("src.agent.engine.client")
    def test_agent_direct_response(self, mock_client):
        # Mock LLM returning a direct answer without tool calls
        mock_response = MagicMock()
        mock_response.content = "Hello! I am doing well."
        mock_response.model_dump.return_value = {"tool_calls": None}
        mock_client.chat_completion.return_value = mock_response

        response = self.engine.run("Hi")
        self.assertEqual(response, "Hello! I am doing well.")
        mock_client.chat_completion.assert_called_once()

    @patch("src.agent.engine.client")
    def test_agent_tool_call_flow(self, mock_client):
        # First call: LLM requests tool call (read_file)
        tool_call_response = MagicMock()
        tool_call_response.content = None
        tool_call_response.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "read_file",
                        "arguments": '{"path": "test_data.txt"}'
                    }
                }
            ]
        }

        # Second call: LLM returns final answer after receiving tool output
        final_response = MagicMock()
        final_response.content = "The file content is: This is a test content for the agent to read."
        final_response.model_dump.return_value = {"tool_calls": None}

        mock_client.chat_completion.side_effect = [tool_call_response, final_response]

        response = self.engine.run("Read test_data.txt")
        self.assertIn("This is a test content", response)
        self.assertEqual(mock_client.chat_completion.call_count, 2)

    @patch("src.agent.engine.client")
    def test_agent_tool_error_handling(self, mock_client):
        # First call: LLM requests tool call with invalid path / non-existent file
        tool_call_response = MagicMock()
        tool_call_response.content = None
        tool_call_response.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "read_file",
                        "arguments": '{"path": "non_existent.txt"}'
                    }
                }
            ]
        }

        # Second call: LLM corrects itself or responds after seeing error
        final_response = MagicMock()
        final_response.content = "Sorry, that file does not exist."
        final_response.model_dump.return_value = {"tool_calls": None}

        mock_client.chat_completion.side_effect = [tool_call_response, final_response]

        response = self.engine.run("Read non_existent.txt")
        self.assertIn("does not exist", response)
        self.assertEqual(mock_client.chat_completion.call_count, 2)

if __name__ == "__main__":
    unittest.main()
