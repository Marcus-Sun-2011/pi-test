import unittest
from unittest.mock import MagicMock, patch
from src.agent.engine import AgentEngine

class TestMockAgentFlow(unittest.TestCase):
    @patch("src.agent.engine.client")
    def test_agent_loop_with_tool_call_mock(self, mock_client):
        # Mock first response: call tool 'get_current_time'
        mock_response_1 = MagicMock()
        mock_response_1.content = "Let me check the time."
        mock_response_1.model_dump.return_value = {
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "get_current_time",
                        "arguments": "{}"
                    }
                }
            ]
        }

        # Mock second response: final answer
        mock_response_2 = MagicMock()
        mock_response_2.content = "The current time has been checked successfully."
        mock_response_2.model_dump.return_value = {
            "tool_calls": []
        }

        mock_client.chat_completion.side_effect = [mock_response_1, mock_response_2]

        engine = AgentEngine()
        result = engine.run("What time is it?")
        
        self.assertIn("time", result.lower())
        self.assertEqual(mock_client.chat_completion.call_count, 2)

if __name__ == "__main__":
    unittest.main()
