from src.agent.engine import engine

def main():
    print("--- Welcome to Local Agent Studio ---")
    print("Type 'quit' or 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        response = engine.run(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()
