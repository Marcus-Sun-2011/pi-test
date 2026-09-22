from typing import List, Dict, Any
from src.core.config import settings
from src.utils.logger import logger
import time

class SecurityGuard:
    def __init__(self):
        # Define tools that require confirmation (high risk)
        self.high_risk_tools = ["delete_file", "run_command"] 

    def needs_confirmation(self, tool_name: str) -> bool:
        """Determines if a tool execution requires user intervention."""
        return tool_name in self.high_risk_tools

    def confirm_action(self, action_description: str) -> bool:
        """Prompt the user for confirmation of a high-risk action."""
        print(f"\n[SECURITY ALERT] High-risk action requested: {action_description}")
        # In a production environment with a proper UI/CLI, this would be more sophisticated.
        confirm = input("Confirm execution? (y/N): ").lower()
        return confirm == 'y'

guard = SecurityGuard()
