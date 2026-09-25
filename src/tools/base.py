from typing import Any, Dict, Type
from pydantic import BaseModel, Field
from src.core.exceptions import ToolExecutionError
from src.utils.logger import logger

class ToolInput(BaseModel):
    """Base class for tool inputs."""
    pass

class SkillDefinition:
    """Base class for skills (logical groupings of related tools)."""
    name: str = ""
    description: str = ""

    def __init__(self):
        pass

class BaseTool:
    name: str = ""
    description: str = ""
    input_schema: Type[ToolInput] = None

    def __init__(self):
        pass

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executes the tool and returns a result dictionary."""
        try:
            if self.input_schema:
                # Validate input against schema
                validated_data = self.input_schema(**kwargs)
                args = validated_data.model_dump()
            else:
                args = kwargs

            logger.info(f"Executing tool: {self.name}")
            result = self._run(args)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            raise ToolExecutionError(f"Failed to execute {self.name}: {str(e)}")

    def _run(self, args: Dict[str, Any]) -> Any:
        """Override this method in subclasses to implement the logic."""
        raise NotImplementedError("Subclasses must implement _run()")
