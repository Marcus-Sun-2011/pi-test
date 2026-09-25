import unittest
from unittest.mock import MagicMock, patch
from src.agent.engine import AgentEngine

class TestAgentEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AgentEngine()

    @patch("src.agent.engine.client")
    def test_agent_direct_response(self, mock_client):
        # Test case where the model provides a direct answer without calling any tools
        mock_response = MagicMock()
        mock_response.content = "The capital of France is Paris."
        mock_response.model_dump.return_value = {"tool_calls": None}
        mock_client.chat_completion.return_value = mock_response

        response = self.engine.run("What is the capital of France?")
        self.assertIn("Paris", response)
        self.assertEqual(mock_client.chat_completion.call_count, 1)

    @patch("src.agent.engine.client")
    def test_agent_tool_call_flow(self, mock_client):
        # Test case where the model calls a tool and then provides a final response
        mock_tool_call = MagicMock()
        mock_tool_call.content = None
        mock_tool_call.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "read_file", "arguments": '{"path": "test.txt"}'}
                }
            ]
        }
        mock_final_response = MagicMock()
        mock_final_response.content = "The content of test.txt is: Hello World."
        mock_final_response.model_dump.return_value = {"tool_calls": None}

        mock_client.chat_completion.side_effect = [mock_tool_call, mock_final_response]

        response = self.engine.run("Read test.txt")
        self.assertIn("Hello World", response)
        self.assertEqual(mock_client.chat_completion.call_count, 2)

    @patch("src.agent.engine.client")
    def test_agent_multiple_tool_calls_in_one_turn(self, mock_client):
        # Test case where LLM calls multiple tools in a single response
        first_call = MagicMock()
        first_call.content = None
        first_call.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "list_files", "arguments": '{"path": "."}'}
                },
                {
                    "id": "call_2",
                    "type": "function",
                    "function": {"name": "read_file", "arguments": '{"path": "test.txt"}'}
                }
            ]
        }

        second_call = MagicMock()
        second_call.content = "I've listed the files and read test.txt."
        second_call.model_dump.return_value = {"tool_calls": None}

        mock_client.chat_completion.side_effect = [first_call, second_call]

        # The engine should iterate through both tool calls in the first response
        response = self.engine.run("List files and read test.txt")
        self.assertIn("I've listed", response)
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

    @patch("src.agent.engine.client")
    def test_agent_error_feedback_loop(self, mock_client):
        # Test case where a tool returns an error and the model corrects its input in the next turn
        tool_error_call = MagicMock()
        tool_error_call.content = None
        tool_error_call.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "read_file", "arguments": '{"path": "wrong_path.txt"}'}
                }
            ]
        }

        # The second call is the model correcting itself after seeing a ToolExecutionError or similar
        correction_call = MagicMock()
        correction_call.content = "I apologize, let me try that again with the correct path."
        correction_call.model_dump.return_value = {"tool_calls": None}

        mock_client.chat_completion.side_effect = [tool_error_call, correction_call]

        response = self.engine.run("Read wrong_path.txt")
        self.assertIn("correct path", response)
        self.assertEqual(mock_client.chat_completion.call_count, 2)

if __name__ == "__main__":
    unittest.main()
