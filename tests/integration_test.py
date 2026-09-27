import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.agent.engine import AgentEngine
from src.core.exceptions import ValidationError, ToolExecutionError, SecurityBlockError
from src.core.workspace import workspace_manager
from src.tools.registry import registry

class TestAgentIntegrationSuite(unittest.TestCase):
    def setUp(self):
        self.engine = AgentEngine()

    @patch('src.agent.model_client.client.chat_completion')
    def test_successful_tool_call_flow(self, mock_chat_completion):
        """
        Test a successful multi-turn flow:
        Turn 1: Model requests a tool call (e.g., list_files).
        Turn 2: Model receives tool result and provides a final answer.
        """
        # First response: Model decides to call 'list_files'
        first_response = MagicMock()
        first_response.content = "I will list the files in the workspace."
        first_response.model_dump.return_value = {
            "content": "I will list the files in the workspace.",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "list_files",
                        "arguments": '{"path": "."}'
                    }
                }
            ]
        }

        # Second response: Model provides final answer after seeing the tool output
        second_response = MagicMock()
        second_response.content = "Here are the files in your workspace."
        second_response.model_dump.return_value = {
            "content": "Here are the files in your workspace.",
            "tool_calls": []
        }

        mock_chat_completion.side_effect = [first_response, second_response]

        # Run the engine
        response = self.engine.run("Show me the files.")
        
        # Verify result
        self.assertEqual(response, "Here are the files in your workspace.")
        self.assertEqual(mock_chat_completion.call_count, 2)

    @patch('src.agent.model_client.client.chat_completion')
    def test_error_handling_and_self_correction_loop(self, mock_chat_completion):
        """
        Test the error recovery feedback loop:
        Turn 1: Model calls a tool with invalid arguments or triggers an error.
        Turn 2: Engine catches the exception, feeds error message back to model.
        Turn 3: Model receives error feedback, adjusts parameters, and succeeds.
        """
        # Response 1: Model calls tool with bad argument
        resp_1 = MagicMock()
        resp_1.content = "Let me read a file."
        resp_1.model_dump.return_value = {
            "content": "Let me read a file.",
            "tool_calls": [
                {
                    "id": "call_err",
                    "type": "function",
                    "function": {
                        "name": "read_file",
                        "arguments": '{"path": "non_existent_file.txt"}'
                    }
                }
            ]
        }

        # Response 2: Model receives error feedback and responds with correction
        resp_2 = MagicMock()
        resp_2.content = "The file was not found. Let me list files instead."
        resp_2.model_dump.return_value = {
            "content": "The file was not found. Let me list files instead.",
            "tool_calls": [
                {
                    "id": "call_success",
                    "type": "function",
                    "function": {
                        "name": "list_files",
                        "arguments": '{}'
                    }
                }
            ]
        }

        # Response 3: Final answer
        resp_3 = MagicMock()
        resp_3.content = "I have listed the directory successfully after the error."
        resp_3.model_dump.return_value = {
            "content": "I have listed the directory successfully after the error.",
            "tool_calls": []
        }

        mock_chat_completion.side_effect = [resp_1, resp_2, resp_3]

        response = self.engine.run("Read a missing file and handle it.")
        
        self.assertIn("listed the directory", response)
        self.assertEqual(mock_chat_completion.call_count, 3)

    def test_security_sandbox_boundary(self):
        """
        Test security boundary checks:
        Ensure that attempts to traverse directories (e.g. '../../etc/passwd') 
        are strictly intercepted by the WorkspaceManager.
        """
        unsafe_paths = [
            "../outside.txt",
            "../../windows/win.ini",
            "../../../etc/passwd"
        ]
        
        for path in unsafe_paths:
            with self.subTest(path=path):
                with self.assertRaises(SecurityBlockError):
                    workspace_manager.validate_and_resolve(path)

if __name__ == "__main__":
    unittest.main()
