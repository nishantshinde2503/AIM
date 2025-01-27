import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Database configuration
DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

# Generative AI API key
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
