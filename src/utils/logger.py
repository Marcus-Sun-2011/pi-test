from loguru import logger
import sys
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure loguru logger
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/agent_studio.log", rotation="10 MB", retention="7 days", level="DEBUG")
