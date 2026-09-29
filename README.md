# Local Agent Studio

A professional, local-first AI Agent framework designed to connect with LM Studio's OpenAI-compatible API. 

## Overview
Local Agent Studio provides a robust environment for building autonomous agents using local LLMs (via LM Studio). It features an advanced tool execution engine, multi-turn reasoning capabilities, and strict security guardrails.

## Features
- **Local Privacy**: No data leaves your machine. All inference is performed locally via LM Studio.
- **Tool Integration**: Seamless integration for function calling. Supports complex chains of actions (e.g., "search online then summarize a specific file").
- **Security & Safety**:
    - **Security Guard**: Automatically detects and prompts for confirmation on high-risk tools (like shell commands or deletions).
    - **Workspace Sandbox**: All file system operations are strictly validated against a predefined workspace path to ensure safety.
- **Advanced Reasoning**: Supports "Chain of Thought" processing, allowing the model to plan several steps before acting.

## Getting Started

### Prerequisites
1.  **LM Studio**: Install from [lmstudio.ai](https://lmstudio.ai).
2.  **Model Support**: Load a capable model (e.g., Llama 3, Mistral) and start the Local Server (default port: `1234`).

### Installation
```bash
git clone <repository_url>
cd local_agent_studio
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_API_KEY=lm-studio
MODEL_NAME=your_loaded_model_name
WORKSPACE_PATH=./workspace
```

### Basic Usage
```python
from src.agent.engine import engine

response = engine.run("List the files in my workspace and tell me about the one with the largest size.")
print(response)
```

## Architecture
- **Engine**: Core loop for memory, tool calling, and LLM interaction.
- **Tool System**: A registry of capabilities (file operations, web search, time).
- **Safety Layer**: Intercepts high-risk actions before execution.
- **Memory**: Maintains conversation context for consistent multi-turn interactions.

## Examples
See the `examples/` directory for sample scripts demonstrating complex task handling and tool chains.
