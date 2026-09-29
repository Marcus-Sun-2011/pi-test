from loguru import logger
import sys
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure loguru logger
logger.remove()
logger.add(sys.stderr, level='INFO')
logger.add('logs/agent_studio.log', rotation='10 MB', retention='7 days', level='DEBUG')

def log_tool_execution(tool_name: str, args: dict, result: any):
    '''Helper to log successful tool execution.'''
    logger.info(f'SUCCESS | Tool: {tool_name} | Args: {args} | Result: {result}')

def log_tool_failure(tool_name: str, args: dict, error: Exception):
    '''Helper to log failed tool execution with details.'''
    logger.error(f'FAILURE | Tool: {tool_name} | Args: {args} | Error Type: {type(error).__name__} | Message: {str(error)}')
