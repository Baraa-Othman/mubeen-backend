import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # On Render/cloud: set FIREBASE_CREDENTIALS_JSON to the full JSON string.
    # Locally: FIREBASE_CREDENTIALS_PATH pointing to the key file still works.
    FIREBASE_CREDENTIALS_JSON: str = os.getenv("FIREBASE_CREDENTIALS_JSON", "")
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")

    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    # Temperature per feature
    ESSAY_TEMPERATURE: float = 0.3
    TRANSLATION_TEMPERATURE: float = 0.2
    DOCUMENT_TEMPERATURE: float = 0.7


settings = Settings()
