"""
JeevanGrid Core Configuration Module
Manages application settings, environment variables, security tokens, and service URLs.
"""

from functools import lru_cache
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # General App Config
    APP_NAME: str = "JeevanGrid Disaster Intelligence Platform"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"

    # Security & Auth
    SECRET_KEY: str = Field(
        default="dev-insecure-secret-key-change-in-production-min-32-chars",
        description="Secret key for JWT signature"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ALGORITHM: str = "HS256"

    # Server Binding
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # CORS Configuration
    ALLOWED_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    @field_validator("ALLOWED_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration (PostgreSQL + PostGIS)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "jeevangrid_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jeevangrid_db"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/jeevangrid_db"

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"

    # Disaster Simulation & Demo Controls
    ENABLE_DEMO_SIMULATION_MODE: bool = True
    DEFAULT_SIMULATION_SCENARIO: str = "assam_brahmaputra_flood_2026"

    # AI/ML & LLM Provider Configuration
    AI_PROVIDER: str = "mock"  # Options: "mock", "gemini", "openai", "anthropic"
    AI_API_KEY: str = ""
    AI_MODEL_NAME: str = "gemini-1.5-flash"
    AI_TEMPERATURE: float = 0.2
    AI_REQUEST_TIMEOUT_SECONDS: float = 10.0
    ENABLE_AI_RECOMMENDATION_ENGINE: bool = True
    ML_MODEL_REGISTRY_PATH: str = "ai_ml/models/"
    USE_MOCK_ML_INFERENCE: bool = True
    # Real-Time Operations & Alerts Configuration (Phase 8)
    REALTIME_ENABLED: bool = True
    ALERT_DEDUPLICATION_WINDOW_SECONDS: int = 300
    REALTIME_HEARTBEAT_SECONDS: int = 30
    MAX_IN_MEMORY_EVENTS: int = 1000


@lru_cache()
def get_settings() -> Settings:
    """Provides a cached singleton instance of Settings."""
    return Settings()


settings = get_settings()
