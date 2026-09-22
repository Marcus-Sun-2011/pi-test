import os
from src.core.config import settings

class WorkspaceManager:
    def __init__(self, base_dir: str = None):
        # If no base_dir is provided in config or as argument, use current directory
        self.base_dir = os.path.abspath(base_dir) if base_dir else os.path.abspath(".")

    def is_safe_path(self, file_path: str) -> bool:
        """Check if the given path is within the allowed workspace."""
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith(self.base_dir)

    def get_safe_path(self, file_path: str) -> str:
        """Resolve and validate a path against the workspace limits."""
        abs_path = os.path.abspath(file_path)
        if not abs_path.startswith(self.base_dir):
            raise PermissionError(f"Security Error: Path {file_path} is outside of the allowed workspace.")
        return abs_path

# Global instance for use by tools
workspace_manager = WorkspaceManager()
