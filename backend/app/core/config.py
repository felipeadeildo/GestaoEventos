import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    API_V1_STR: str = "/api/v1"

    SUPERUSER_EMAIL: str = "admin@localhost"
    SUPERUSER_PASSWORD: str = "admin"


settings = Settings()
