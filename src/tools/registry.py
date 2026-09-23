from typing import Dict, List, Type
from src.tools.base import BaseTool

class ToolRegistry:
    def __init__(self):
        # Maps tool name -> BaseTool instance
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool_instance: BaseTool):
        """Registers a new tool by its name."""
        if not tool_instance.name:
            raise ValueError("Tool must have a name.")
        if tool_instance.name in self._tools:
            raise ValueError(f"Tool with name '{tool_instance.name}' is already registered.")
        self._tools[tool_instance.name] = tool_instance

    def get_all_tools(self) -> List[BaseTool]:
        """Returns a list of all registered tools."""
        return list(self._tools.values())

    def get_tool(self, name: str) -> BaseTool:
        """Gets a specific tool by name."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found.")
        return self._tools[name]

    def get_tools_info(self) -> list:
        """Returns a representation of all tools for the LLM prompt."""
        tools_info = []
        for tool in self.get_all_tools():
            if tool.input_schema is None:
                properties = {}
            else:
                # Use Pydantic's model_json_schema to get the correct structure for the LLM
                # Since we just need the properties part for OpenAI-compatible tools:
                properties = tool.input_schema.model_json_schema().get("properties", {})

            tools_info.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": list(tool.input_schema.model_fields.keys()) if tool.input_schema else []
                    }
                }
            })
        return tools_info


# Global registry instance
registry = ToolRegistry()

# Auto-discover and import all tool implementations so they register themselves
import importlib
import pkgutil
import src.tools.implementations

for _, module_name, _ in pkgutil.walk_packages(src.tools.implementations.__path__, src.tools.implementations.__name__ + "."):
    importlib.import_module(module_name)

