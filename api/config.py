import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_CONFIG=os.getenv("DATABASE_URL")
# GEMINI_API_KEY=