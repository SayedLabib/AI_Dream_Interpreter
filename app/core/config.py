import os
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    app_name: str = "Dream AI Interpreter"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow extra fields to be ignored rather than causing validation errors
        extra = "ignore"
        # Allow population by field name and alias
        populate_by_name = True

settings = Settings()