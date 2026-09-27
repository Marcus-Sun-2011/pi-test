from typing import List, Dict, Any
from src.core.config import settings
from src.utils.logger import logger
import os
from pathlib import Path
from src.core.exceptions import SecurityBlockError
from src.core.workspace import workspace_manager

class SecurityGuard:
    def __init__(self):
        # Define tools that require confirmation (high risk)
        # These are actions that could potentially damage the system or data.
        self.high_risk_tools = ["delete_file", "run_command"] 

    def validate_path(self, path_str: str) -> Path:
        """
        Validates that a given path is within the allowed workspace.
        Ensures no directory traversal or out-of-bounds access occurs by delegating 
        to WorkspaceManager.
        
        Returns:
            Path: The resolved absolute system path if valid.
        Raises:
            SecurityBlockError: If the path is outside the sandbox.
        """
        # Delegate to workspace_manager for robust resolution and validation
        validated_path = workspace_manager.validate_and_resolve(path_str)
        return validated_path

    def needs_confirmation(self, tool_name: str) -> bool:
        """Determines if a tool execution requires user intervention based on its risk level."""
        return tool_name in self.high_risk_tools

    def confirm_action(self, action_description: str) -> bool:
        """Prompt the user for confirmation of a high-risk action with clear context."""
        print(f"\n[SECURITY ALERT] High-risk action requested:")
        print(f"Description: {action_description}")
        # In a production environment, this would be integrated into a TUI or Web UI.
        confirm = input("Do you want to proceed with this operation? (y/N): ").lower()
        return confirm == 'y'

guard = SecurityGuard()
