import sys
from src.agent.engine import engine
from src.utils.logger import logger

def main():
    logger.info("Starting Agent Studio...")
    
    # The logic is now encapsulated in the Engine
    user_input = input("User: ")
    response = engine.run(user_input)
    print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
