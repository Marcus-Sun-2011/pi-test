from typing import Optional
from loguru import logger

# Custom Exception classes for granular error handling
class AgentError(Exception):
    """Base error for all agent-related issues."""
    pass

class ConnectionError(AgentError):
    """Raised when the connection to LM Studio/OpenAI fails."""
    pass

class ToolExecutionError(AgentError):
    """Raised when a specific tool (e.g., file_read) encounters an error during execution."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception

class SecurityBlockError(ToolExecutionError):
    """Raised when an action is explicitly blocked by the SafetyGuard."""
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
