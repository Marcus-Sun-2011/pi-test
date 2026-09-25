import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.agent.engine import engine
from src.utils.logger import logger

def run_test_case(name, user_input):
    print(f"\n{'='*60}")
    print(f"TEST CASE: {name}")
    print(f"Input: {user_input}")
    print(f"{'-'*60}")
    try:
        result = engine.run(user_input)
        print(f"\nFinal Result from Model:\n{result}")
    except Exception as e:
        print(f"\n[ERROR] An unexpected exception occurred: {e}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # 1. Multi-Tool Interaction Test
    # The model should decide to call multiple tools (e.g., time and maybe something else or just complex planning)
    run_test_case("Multi-Tool Chain", "What is the current time, and what day of the week is it today?")

    # 2. Error Handling & Recovery Test
    # This should trigger a ToolExecutionError/ValidationError and see if the model tries to fix itself.
    run_test_case("Error Feedback Loop", "Read the contents of a file named 'non_existent_file.txt'.")

    # 3. Complex Reasoning with Tools
    run_test_case("Complex Reasoning", "Find out what time it is, and then tell me how many seconds are in that day.")
