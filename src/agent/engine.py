from typing import List, Dict, Any, Optional
from src.tools.registry import registry
from src.agent.model_client import client
from src.agent.memory import Memory
from src.core.config import settings
from src.utils.logger import logger
import json
from src.core.security import guard
from src.core.exceptions import ToolExecutionError, ValidationError

class AgentEngine:
    def __init__(self):
        self.memory = Memory()
        self.max_iterations = settings.max_iterations

    def run(self, user_input: str) -> str:
        """Main entry point for a single conversation turn."""
        self.memory.add_message("user", user_input)
        
        current_iteration = 0
        while current_iteration < self.max_iterations:
            current_iteration += 1
            logger.info(f"Iteration {current_iteration} starting...")

            # Get history from memory
            history = self.memory.get_history()
            
            # Call the model
            response = client.chat_completion(history)
            content = response.content
            
            # Log the result for debugging
            logger.info(f"Model Response: {content}")

            # Check if it's a tool call
            if "tool_calls" in response.model_dump() and response.model_dump()["tool_calls"]:
                tool_calls = response.model_dump()["tool_calls"]
                
                for tool_call in tool_calls:
                    tool_name = tool_call["function"]["name"]
                    args_raw = tool_call["function"]["arguments"]
                    # Ensure args is a dictionary (some clients return string, some dict)
                    args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                    
                    # Security Check
                    if guard.needs_confirmation(tool_name):
                        prompt = f"Execute {tool_name} with arguments {args}?"
                        if not guard.confirm_action(prompt):
                            logger.warning(f"Action cancelled by user for tool: {tool_name}")
                            self.memory.add_message("system", f"The request to use {tool_name} was denied by the system.")
                            continue

                    logger.info(f"Tool Call Executing: {tool_name} with args {args}")
                    
                    try:
                        tool = registry.get_tool(tool_name)
                        result = tool.execute(**args)
                        # Success path - inform the model of success and the result
                        self.memory.add_message("system", f"Tool {tool_name} successfully executed. Result: {result['result']}")
                    except ValidationError as ve:
                        # Inform the model about specific validation errors so it can correct them
                        logger.error(f"Validation Error for tool '{tool_name}': {ve}")
                        self.memory.add_message("system", f"Validation Error for tool '{tool_name}': {str(ve)}. Please check your parameters.")
                    except ToolExecutionError as tee:
                        # Inform the model of a runtime error in the tool logic
                        logger.error(f"Tool Execution Error for '{tool_name}': {tee}")
                        self.memory.add_message("system", f"Tool Execution Error for '{tool_name}': {str(tee)}")
                    except Exception as e:
                        # Catch-all for unexpected errors
                        logger.exception(f"Unexpected error during execution of {tool_name}")
                        self.memory.add_message("system", f"An unexpected system error occurred while executing tool '{tool_name}'.")
                    continue
            else:
                # No tool calls, it's a final answer or intermediate thought
                self.memory.add_message("assistant", content)
                return content

        logger.warning(f"Maximum iterations ({self.max_iterations}) reached.")
        return "Maximum steps reached. Please try again with a more specific prompt."

# Global instance for simplicity
engine = AgentEngine()
