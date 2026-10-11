import os
from dotenv import load_dotenv
from app.core.paths import data_dir

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DentalAI Clinic")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(data_dir() / 'dental.db').as_posix()}"
    )

settings = Settings()