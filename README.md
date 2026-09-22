# Local Agent Studio

A professional, local-first AI Agent framework designed to connect with LM Studio's OpenAI-compatible API. 

## Features
- **Local Privacy**: No data leaves your machine. All inference is done via LM Studio.
- **Tool Integration**: Built-in support for function calling and tool execution.
- **Safety First**: Includes a security layer to restrict file system access to specific workspaces and requires human confirmation for high-risk actions.
- **Extensible Architecture**: Modular design allows you to easily plug in new tools and capabilities.

## Setup & Installation

1.  **Install LM Studio**: 
    Download and install [LM Studio](https://lmstudio.ai/).
2.  **Launch a Model**:
    Load your preferred model (e.g., Llama 3, Mistral) in the "Local Server" tab.
    Ensure the server is running on `http://localhost:1234`.
3.  **Clone this project & Install Dependencies**:
    ```bash
    git clone <your-repo-url>
    cd local_agent_studio
    pip install -r requirements.txt
    ```
4.  **Configuration**:
    Create a `.env` file in the root directory:
    ```env
    MODEL_NAME=lmstudio
    API_BASE_URL=http://localhost:1234/v1
    # API_KEY is required by the SDK but not used by LM Studio
    API_KEY=lm-studio
    MAX_ITERATIONS=10
    ```

## Usage

Run the application from the root directory:
```bash
python src/main.py
```
The system will prompt you to interact with the AI Agent. It can read files, answer questions, and perform other tools as requested.

## Architecture Highlights
- **Agent Loop**: Implements a ReAct pattern (Reasoning + Acting).
- **Security Gate**: A dedicated `SecurityGuard` prevents unauthorized actions and ensures file safety.
- **Workspace Shield**: Ensures the agent cannot access files outside of its intended scope.
