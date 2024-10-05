import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# API settings
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY")

# CLI settings
CLI_VERSION = os.getenv("CLI_VERSION", "0.1.0")
