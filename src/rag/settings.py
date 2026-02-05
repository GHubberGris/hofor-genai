from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    OPENAI_API_KEY: str | None = Field(default=None, repr=False)
    QDRANT_URL: str = Field(default="http://localhost:6333")
    COLLECTION: str = Field(default="hofor_kravspec")
    EMBED_MODEL: str = Field(default="text-embedding-3-small")
    CHAT_MODEL: str = Field(default="gpt-4o-mini")
    TOP_K: int = Field(default=5)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
