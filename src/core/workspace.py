import os
from pathlib import Path
from src.core.config import settings
from src.core.exceptions import SecurityBlockError

class WorkspaceManager:
    def __init__(self):
        # Ensure the workspace path is absolute and resolved
        raw_path = settings.workspace_dir
        if not raw_path.startswith(("/", "\\")):
            raw_path = os.path.abspath(raw_path)
        self.base_path = Path(raw_path).resolve()

    def validate_and_resolve(self, input_path: str) -> Path:
        """
        Strictly validates that the requested path is within the allowed workspace.
        Prevents directory traversal (e.g., ../../etc/passwd).
        """
        # 1. Convert to absolute and resolve symlinks/relative components
        requested_path = Path(input_path).resolve()

        # 2. Check if it's inside the workspace
        # We check if the base_path is a parent of (or equal to) requested_path
        if not str(requested_path).startswith(str(self.base_path)):
            # Extra check for cases where paths might be technically valid but outside our scope
            if self.base_path != requested_path and self.base_path not in requested_path.parents:
                raise SecurityBlockError(f"Security Violation: Path '{input_path}' is outside the workspace.")

        return requested_path

    def get_full_path(self, path_str: str) -> str:
        """Returns a string representation of the validated path."""
        validated = self.validate_and_resolve(path_str)
        return str(validated)

# Global instance for tools to use
workspace_manager = WorkspaceManager()
