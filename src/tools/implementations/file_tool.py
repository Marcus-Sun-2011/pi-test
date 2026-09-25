from src.tools.base import BaseTool
from typing import Dict, Any
from src.core.security import guard
import os
from src.core.exceptions import ToolExecutionError, ValidationError

class FileReadTool(BaseTool):
    def __init__(self):
        pass

    def _run(self, args: Dict[str, Any]) -> Any:
        path_raw = args.get("path")
        if not path_raw:
            raise ValidationError("FileReadTool requires a 'path' argument.")
        
        # Safety Check: Ensure the requested path is within our workspace
        try:
            path = guard.validate_path(path_raw)
        except Exception as e:
            # Re-raise as ToolExecutionError to be caught by engine's error handler
            raise ToolExecutionError(f"Security/Path Error: {str(e)}")
        
        try:
            with open(str(path), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise ToolExecutionError(f"File not found at path: {path}")
        except Exception as e:
            raise ToolExecutionError(f"Failed to read file: {str(e)}")

class ListFilesTool(BaseTool):
    def __init__(self):
        pass

    def _run(self, args: Dict[str, Any]) -> Any:
        path_raw = args.get("path", ".")
        if not path_raw:
            raise ValidationError("ListFilesTool requires a 'path' argument.")
            
        # Safety Check: Ensure the requested path is within our workspace
        try:
            path = guard.validate_path(path_raw)
        except Exception as e:
            raise ToolExecutionError(f"Security/Path Error: {str(e)}")
        
        try:
            return os.listdir(str(path))
        except Exception as e:
            raise ToolExecutionError(f"Failed to list directory at {path}: {str(e)}")

class WriteFileTool(BaseTool):
    def __init__(self):
        pass

    def _run(self, args: Dict[str, Any]) -> Any:
        path_raw = args.get("path")
        if not path_raw:
            raise ValidationError("WriteFileTool requires a 'path' argument.")
        
        # Safety Check: Ensure the requested path is within our workspace
        try:
            path = guard.validate_path(path_raw)
        except Exception as e:
            raise ToolExecutionError(f"Security/Path Error: {str(e)}")
        
        content = args.get("content", "")
        try:
            with open(str(path), 'w', encoding='utf-8') as f:
                f.write(content)
            return "Success"
        except Exception as e:
            raise ToolExecutionError(f"Failed to write file at {path}: {str(e)}")
