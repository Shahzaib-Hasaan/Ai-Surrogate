"""
Application configuration settings.

This module loads and validates environment variables for the application.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.
    
    Attributes:
        DATABASE_URL: PostgreSQL connection string
        SECRET_KEY: Secret key for JWT token generation
        ALGORITHM: Algorithm for JWT encoding (default: HS256)
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes
        ALLOWED_ORIGINS: CORS allowed origins
    """
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200")  # 30 days default
    )
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8081,http://localhost:19000"
    )
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_CHAT_MODEL: str = os.getenv("MISTRAL_CHAT_MODEL", "mistral-large-2512")
    MISTRAL_TITLE_MODEL: str = os.getenv("MISTRAL_TITLE_MODEL", "mistral-small-latest")
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    MAX_RESPONSE_TOKENS: int = int(os.getenv("MAX_RESPONSE_TOKENS", "1000"))
    MAX_CONTEXT_MESSAGES: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))
    
    # Voice Processing (Google Cloud)
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    GOOGLE_CREDENTIALS_JSON: Optional[str] = os.getenv("GOOGLE_CREDENTIALS_JSON", None)
    
    # Search APIs
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert ALLOWED_ORIGINS string to list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    def validate(self) -> None:
        """
        Validate that all required settings are present.
        
        Raises:
            ValueError: If any required setting is missing
        """
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required")


# Create global settings instance
settings = Settings()

# Validate settings on import
settings.validate()
