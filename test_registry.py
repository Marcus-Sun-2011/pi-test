from src.tools.registry import tool_registry, skill_registry, get_all_capabilities

tools = tool_registry.get_all_tools()
skills = skill_registry.get_all_skills()

print(f"Total Tools: {len(tools)}")
for t in tools:
    print(f"  Tool: {t.name}")

print(f"\nTotal Skills: {len(skills)}")
for s in skills:
    print(f"  Skill: {s.name}")

capabilities = get_all_capabilities()
print(f"\nTotal Capabilities: {len(capabilities)}")
