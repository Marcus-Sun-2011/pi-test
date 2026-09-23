from typing import List, Dict, Any
import os
from pydantic import BaseModel, Field
from src.tools.base import BaseTool
from src.core.workspace import workspace_manager
from src.utils.logger import logger

class FileReadTool(BaseTool):
    name = "read_file"
    description = "Reads the content of a file from the workspace."
    
    # Define Pydantic model for input validation
    class ToolInput(BaseModel):
        path: str = Field(..., description="The path to the file relative to the workspace root.")

    input_schema = ToolInput

    def _run(self, args: Dict[str, Any]) -> str:
        file_path = args.get("path")
        # Security Check: Ensure path is within workspace
        full_path = workspace_manager.get_safe_path(file_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

class ListFilesTool(BaseTool):
    name = "list_files"
    description = "Lists the files in a directory within the workspace."
    
    class ToolInput(BaseModel):
        path: str = Field(..., description="The path to the directory (defaulting to root if empty) relative to the workspace.")

    input_schema = ToolInput

    def _run(self, args: Dict[str, Any]) -> str:
        dir_path = args.get("path", ".")
        # Security Check: Ensure path is within workspace
        full_path = workspace_manager.get_safe_path(dir_path)

        try:
            files = os.listdir(full_path)
            return "\n".join(files) if files else "Directory is empty."
        except Exception as e:
            return f"Error listing directory: {str(e)}"

class WriteFileTool(BaseTool):

    name = "write_file"
    description = "Creates or overwrites a file with the provided content in the workspace."
    
    class ToolInput(BaseModel):
        path: str = Field(..., description="The path to the file relative to the workspace root.")
        content: str = Field(..., description="The text content to write into the file.")

    input_schema = ToolInput

    def _run(self, args: Dict[str, Any]) -> str:
        file_path = args.get("path")
        content = args.get("content")
        if not file_path or content is None:
            raise ValueError("Both 'path' and 'content' are required.")

        # Security Check: Ensure path is within workspace
        full_path = workspace_manager.get_safe_path(file_path)

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

from src.tools.registry import registry
registry.register(FileReadTool())
registry.register(ListFilesTool())
registry.register(WriteFileTool())
