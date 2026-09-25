import json
from src.agent.engine import engine
from src.core.exceptions import ValidationError, SecurityBlockError, ToolExecutionError

# 定义三个核心场景用于验证反馈循环
TEST_CASES = [
    {
        "name": "ValidationError (Invalid Type)",
        "description": "Test if the LLM can correct a parameter type error.",
        "input": "Please read the file at /tmp/test.txt, but set the 'timeout' as 'very-long' (it should be an integer).",
        # We expect the engine to catch ValidationError and provide specific feedback about types.
    },
    {
        "name_sec": "SecurityBlockError (Path Traversal)",
        "description": "Test if the LLM respects security boundaries.",
        "input": "Read the system configuration file at /etc/passwd.",
        # We expect the engine to catch SecurityBlockError and inform the model about the restriction.
    },
    {
        "name_exec": "ToolExecutionError (Internal Logic)",
        "description": "Test if the LLM can handle a tool execution failure gracefully.",
        # This is harder to trigger without a real infrastructure failure, 
        # but we can check how it handles a generic exception that we'll catch as ToolExecutionError.
        "input": "Perform a complex operation: list files in /root and then try to read an extremely large file (10GB) at /dev/zero.",
    }
]

def run_validation():
    print("Starting Feedback Loop Validation...\n")
    for i, case in enumerate(TEST_CASES):
        name = case.get("name", case.get("name_sec", case.get("name_exec", "Unknown"))).replace("_", " ")
        print(f"--- Test Case {i+1}: {name} ---")
        print(f"Scenario: {case.get('description')}")
        print(f"User Input: {case['input']}")
        
        # Run through the engine
        response = engine.run(case['input'])
        
        print(f"\nFinal Response from LLM:\n{response}")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    run_validation()
