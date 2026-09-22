from typing import Optional
from loguru import logger

# Custom Exception classes for granular error handling
class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass

class ConnectionError(AgentError):
    """Raised when the connection to LM Studio/OpenAI fails."""
    pass

class ToolExecutionError(AgentError):
    """Raised when a specific tool (e.g., file_read) encounters an error during execution."""
    pass

class ValidationError(AgentError):
    """Raised when input parameters do not meet Pydantic requirements."""
    pass

class TimeoutError(AgentError):
    """Raised when the model or a tool takes too long to respond."""
    pass

def log_error(message: str, exception: Optional[Exception] = None):
    """Helper function to log errors consistently."""
    if exception:
        logger.error(f"{message} | Error: {exception}")
    else:
        logger.error(message)
