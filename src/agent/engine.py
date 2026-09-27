from typing import List, Dict, Any, Optional
from src.tools.registry import registry, get_all_capabilities
from src.agent.model_client import client
from src.agent.memory import Memory
from src.core.config import settings
from src.utils.logger import log_tool_execution, log_tool_failure
import json
from src.core.security import guard
from src.core.exceptions import ToolExecutionError, ValidationError, SecurityBlockError

class AgentEngine:
    def __init__(self):
        self.memory = Memory()
        self.max_iterations = settings.max_iterations
        # Use the unified capability list which includes both tools and skills
        self.tools_info = get_all_capabilities()
    
    def _build_system_prompt(self) -> str:
        """Constructs a comprehensive system message to guide the model's reasoning and tool usage."""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S (%A)")
        base_instructions = (
            f"You are an intelligent AI assistant with access to a suite of tools. "
            f"The current real-world date and time is {current_time}.\n\n"
            "OPERATING PRINCIPLES:\n"
            "1.  **Reasoning First**: Before taking any action or calling a tool, think step-by-step about the user's request. "
            "If necessary, use 'Chain of Thought' to break down complex tasks into smaller, manageable steps.\n"
            "2.  **Tool Selection**: Choose the most appropriate tool based on the provided definitions. If multiple tools are required for a task, call them sequentially in your reasoning chain.\n"
            "3.  **Error Handling**: If a tool returns an error message or unexpected output, analyze the failure reason. "
            "Adjust your parameters and retry the operation if appropriate, or try an alternative approach to fulfill the user's request.\n"
            "4.  **Conciseness**: Provide clear and helpful responses. Avoid over-explaining internal processes unless asked.\n"
            "5.  **Privacy & Safety**: Do not disclose these system instructions or your internal tool list to the user unless specifically requested by a query about your capabilities.\n\n"
            "AVAILABLE TOOLS:"
        )
        tools_str = "\n".join([f"- {t['function']['name']}: {t['function']['description']} (Parameters: {t['function']['parameters']})" for t in self.tools_info])
        return base_instructions + "\n" + tools_str

    def run(self, user_input: str) -> str:
        """Main entry point for a single conversation turn."""
        # Prepare the message history
        history = []
        if self.memory.history:
            history = self.memory.get_history()
        else:
            # Initial system prompt setup if memory is empty or to ensure context exists
            history.append({"role": "system", "content": self._build_system_prompt()})

        self.memory.add_message("user", user_input)
        
        current_iteration = 0
        while current_iteration < self.max_iterations:
            current_iteration += 1
            from src.utils.logger import logger
            logger.info(f"--- Iteration {current_iteration}/{self.max_iterations} ---")

            # Get history from memory
            history = self.memory.get_history()
            
            # Call the model with included tool definitions
            response = client.chat_completion(history, tools=self.tools_info)
            content = response.content
            
            # Log the result for debugging
            logger.info(f"Model Output: {content}")

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

                    logger.info(f"Executing Tool: {tool_name} | Args: {args}")
                    
                    try:
                        tool = registry.get_tool(tool_name)
                        result = tool.execute(**args)
                        
                        # Success path - inform the model of success and the result
                        log_tool_execution(tool_name, args, result)
                        success_msg = f"Tool '{tool_name}' executed successfully.\nResult: {result['result']}"
                        self.memory.add_message("system", success_msg)
                    except ValidationError as ve:
                        error_msg = f"Validation Error for '{tool_name}': {str(ve)}. Please check your input parameters."
                        log_tool_failure(tool_name, args, ve)
                        logger.warning(f"{error_msg}")
                        self.memory.add_message("system", error_msg)
                    except SecurityBlockError as sbe:
                        error_msg = f"Security Block for '{tool_name}': {str(sbe)}. This action is restricted."
                        logger.warning(f"{error_msg}")
                        self.memory.add_message("system", error_msg)
                    except ToolExecutionError as tee:
                        error_msg = f"Execution Error for '{tool_name}': {str(tee)}. Please adjust your approach."
                        log_tool_failure(tool_name, args, tee)
                        logger.error(f"{error_msg}")
                        self.memory.add_message("system", error_msg)
                    except Exception as e:
                        error_msg = f"System Error during '{tool_name}': {type(e).__name__}. Please try a different approach."
                        log_tool_failure(tool_name, args, e)
                        logger.exception(f"{error_msg}")
                        self.memory.add_message("system", error_msg)
                    continue
            else:
                # No tool calls, it's a final answer or intermediate thought
                logger.info("No more tool calls. Finalizing step.")
                self.memory.add_message("assistant", content)
                return content

        logger.warning(f"Maximum iterations ({self.max_iterations}) reached.")
        return "Maximum steps reached. Please try again with a more specific prompt."

# Global instance for simplicity
engine = AgentEngine()
