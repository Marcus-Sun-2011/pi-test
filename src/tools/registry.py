from typing import Dict, List, Type, Union
from src.tools.base import BaseTool, SkillDefinition

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

class SkillRegistry:
    def __init__(self):
        # Maps skill name -> SkillDefinition instance
        self._skills: Dict[str, SkillDefinition] = {}

    def register(self, skill_instance: SkillDefinition):
        """Registers a new skill by its name."""
        if not skill_instance.name:
            raise ValueError("Skill must have a name.")
        if skill_instance.name in self._skills:
            raise ValueError(f"Skill with name '{skill_instance.name}' is already registered.")
        self._skills[skill_instance.name] = skill_instance

    def get_all_skills(self) -> List[SkillDefinition]:
        """Returns a list of all registered skills."""
        return list(self._skills.values())

    def get_skill(self, name: str) -> SkillDefinition:
        """Gets a specific skill by name."""
        if name not in self._skills:
            raise ValueError(f"Skill '{name}' not found.")
        return self._skills[name]

    def get_skills_info(self) -> list:
        """Returns a representation of all skills for the LLM prompt."""
        skills_info = []
        for skill in self.get_all_skills():
            # A Skill is presented to the LLM as a "capability" 
            # It contains its own description and a set of tools it encompasses.
            skills_info.append({
                "type": "function",
                "function": {
                    "name": skill.name,
                    "description": skill.description,
                    "parameters": {
                        "type": "object",
                        "properties": {}, # Skills don't have direct params usually, or they are nested. 
                                         # In our current architecture, skills wrap tools.
                        "required": []
                    }
                }
            })
        return skills_info

def get_all_capabilities() -> list:
    """Combines both tools and skills into a single list of capabilities for the LLM."""
    # We include tools as individual actions and skills as capability clusters.
    # The model can choose either based on its context.
    tools = tool_registry.get_tools_info()
    skills = skill_registry.get_skills_info()
    return tools + skills

# Global registry instance
tool_registry = ToolRegistry()
skill_registry = SkillRegistry()

# Compatibility layer
registry = tool_registry

# Auto-discover and import all tool implementations so they register themselves
import importlib
import pkgutil
import src.tools.implementations

for _, module_name, _ in pkgutil.walk_packages(src.tools.implementations.__path__, src.tools.implementations.__name__ + "."):
    importlib.import_module(module_name)
