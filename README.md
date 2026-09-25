# Local Agent Studio

A professional, local-first AI Agent framework designed to connect with LM Studio's OpenAI-compatible API. 

## Features
- **Local Privacy**: No data leaves your machine. All inference is done via LM Studio.
- **Tool Integration**: Built-in support for function calling and tool execution. Supports multi-turn logic (e.g., "search then read").
- **Safety First**: 
    - **Security Gate**: A dedicated `SecurityGuard` filters out high-risk actions (e.g., shell commands) requiring manual confirmation.
    - **Workspace Shield**: Uses a strict sandbox to ensure all file operations are confined to the configured directory, preventing path traversal.
- **Extensible Architecture**: Modular design allows for easy plugin of new tools and capabilities.

## Capabilities
- **Multi-turn Reasoning**: The agent can handle complex tasks requiring multiple tool calls in sequence.
- **Robust Error Handling**: Automated recovery from common failures like missing files or incorrect parameters.
- **Flexible Search**: Integrated web search with fallback mechanisms.
