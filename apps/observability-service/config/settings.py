"""Configuration settings for the Observability Service."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Service configuration
    PORT: int = 8003
    SERVICE_NAME: str = "Observability Service"
    SERVICE_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"

    # Database configuration
    DATABASE_URL: str = "sqlite:///./observability.db"

    # CORS configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
