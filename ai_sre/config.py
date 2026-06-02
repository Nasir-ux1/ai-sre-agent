import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mock")
    SAFETY_SANDBOX_ENABLED = os.getenv("SAFETY_SANDBOX_ENABLED", "True").lower() == "true"
    MAX_STEPS = int(os.getenv("MAX_STEPS", "5"))

    @classmethod
    def get_api_key(cls):
        if cls.GEMINI_API_KEY:
            return "gemini", cls.GEMINI_API_KEY
        elif cls.OPENAI_API_KEY:
            return "openai", cls.OPENAI_API_KEY
        return "mock", ""