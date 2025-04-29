from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "TEST"

    DB_HOST: str
    DB_PORT: int

    TEST_POSTGRES_DB: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    CLIENT_ID: int
    CLIENT_SECRET: str
    VK_SERVICE_TOKEN: str
    VK_ADMIN_TOKEN: str
    VK_AUTH: str
    REDIRECT_URI: str

    DOMAIN: str
    FRONTEND_HOST: str = "http://localhost:5173"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    @property
    def get_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    @property
    def get_test_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_POSTGRES_DB}"


settings = Settings()
