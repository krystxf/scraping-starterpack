"""Configuration and logging setup for the application"""
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Application configuration
MODEL_NAME = "Qwen/Qwen3-VL-2B-Instruct"
DEFAULT_PORT = 3100
DEFAULT_HOST = "0.0.0.0"
MAX_NEW_TOKENS = 512

# Default prompt for text extraction
DEFAULT_EXTRACTION_PROMPT = (
    "Extract all text from this image. List all visible text exactly as it appears, "
    "including any numbers, letters, or symbols."
)

