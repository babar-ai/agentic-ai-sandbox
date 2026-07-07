import os
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):

    Groq_api_key: str
    TAVILY_API_KEY: str

    model_config = {"env_file": os.path.join(current_dir, ".env")}




settings = Settings()

    