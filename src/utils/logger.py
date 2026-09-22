from loguru import logger
import sys

# Configure loguru to output to stdout/stderr correctly
# Standard configuration is usually enough for basic use cases
logger.add(sys.stderr, level="INFO")
