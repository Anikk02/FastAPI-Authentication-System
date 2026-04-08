import logging
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file='.env',
        extra = 'ignore'
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value:str)->str:
        if not value or len(value.strip())<32:
            raise ValueError("SECRET_KEY must be atleast 32 characters long")
        return value
    
    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_expiry(cls, value:int)->int:
        if value<=0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0")
        return value

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, value:str)->str:
        if not value.startswith(('sqlite://','postgresql+asyncpg://','mysql://')):
            raise ValueError(
                'DATABASE_URL must start with sqlite://, postgresql+asyncpg://, or mysql://'
            )
        return value
    

try:
    settings = Settings()
    logger.info("Application configuration loaded successfully")
except Exception as e:
    logger.exception("Failed to load application configuration")
    raise RuntimeError(f"Configuration error: {e}") from e

