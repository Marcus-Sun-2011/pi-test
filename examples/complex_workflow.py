from src.agent.engine import engine

def main():
    # This example demonstrates a complex task where the model needs to 
    # perform multiple steps (list files, then select one based on content/size)
    prompt = (
        "List all files in the current directory and find the one that seems "
        "most interesting related to 'data'. Then read its content and provide a summary."
    )
    
    print(f"--- Complex Task Demo ---")
    print(f"Task: {prompt}")
    
    response = engine.run(prompt)
    print(f"\nFinal Result:\n{response}")

if __name__ == "__main__":
    main()
