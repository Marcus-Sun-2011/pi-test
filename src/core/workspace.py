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
        # Automatically create the workspace directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)

    def validate_and_resolve(self, input_path: str) -> Path:
        """
        Strictly validates that the requested path is within the allowed workspace.
        Prevents directory traversal (e.g., ../../etc/passwd) and prefix-matching bugs.
        """
        if not input_path:
            raise SecurityBlockError("Security Violation: Empty path is not allowed.")

        path_obj = Path(input_path)
        if not path_obj.is_absolute():
            requested_path = (self.base_path / path_obj).resolve()
        else:
            requested_path = path_obj.resolve()

        # Check if requested_path is inside base_path
        try:
            requested_path.relative_to(self.base_path)
        except ValueError:
            raise SecurityBlockError(f"Security Violation: Path '{input_path}' is outside the workspace sandbox.")

        return requested_path

    def get_full_path(self, path_str: str) -> str:
        """Returns a string representation of the validated path."""
        validated = self.validate_and_resolve(path_str)
        return str(validated)

    # Compatibility methods
    def is_safe_path(self, path_str: str) -> bool:
        """Checks if a path is safe and inside the workspace without raising an error."""
        try:
            self.validate_and_resolve(path_str)
            return True
        except (SecurityBlockError, Exception):
            return False

    def get_safe_path(self, path_str: str) -> Path:
        """Returns the safe path or raises PermissionError/SecurityBlockError."""
        try:
            return self.validate_and_resolve(path_str)
        except SecurityBlockError as e:
            raise PermissionError(str(e))

# Global instance for tools to use
workspace_manager = WorkspaceManager()
