from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_NAME: str
    DB_USER: str
    DB_HOST: str
    DB_PASS: str
    DB_PORT: int

    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_HOST: str
    TEST_DB_PASS: str
    TEST_DB_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    VK_CLIENT_ID: int
    VK_CLIENT_SECRET: str
    VK_SERVICE_TOKEN: str
    VK_AUTH: str
    CLIENT_ID: int
    CLIENT_SECRET: str
    REDIRECT_URI: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_test_database_url(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


settings = Settings()
