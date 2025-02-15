import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
VENICE_API_KEY = os.getenv("VENICE_API_KEY")

# Constants
PLACEHOLDER_IMAGE_URL = "https://via.placeholder.com/512x512.png?text=DAO+Image"

# Validation
if not TAVILY_API_KEY or not VENICE_API_KEY:
    print("Warning: Missing API keys in environment variables")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) 