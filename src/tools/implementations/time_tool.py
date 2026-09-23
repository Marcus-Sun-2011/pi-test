from typing import Dict, Any
import datetime
from pydantic import BaseModel
from src.tools.base import BaseTool

class GetCurrentTimeTool(BaseTool):
    name = "get_current_time"
    description = "Returns the current real-world date, time, and day of the week."

    class ToolInput(BaseModel):
        pass

    input_schema = ToolInput

    def _run(self, args: Dict[str, Any]) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S (%A)")

from src.tools.registry import registry
registry.register(GetCurrentTimeTool())
