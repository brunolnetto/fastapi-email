from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self
from pydantic import model_validator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore"
    )
    DOMAIN: str = 'localhost'

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str 
    SENDER_EMAIL: str
    CONTANT_URL: str

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "email_events"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"

    @model_validator(mode="after")
    def are_email_credentials_set(self) -> Self:
        credentials=[
            self.SMTP_SERVER, 
            self.SMTP_PORT, 
            self.SMTP_USERNAME, 
            self.SMTP_PASSWORD, 
            self.SENDER_EMAIL
        ]
        return all(credentials)
    
    @property
    def database_url(self) -> str:
        db_scheme="postgresql+asyncpg"
        db_route=f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        db_credentials=f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
        return f"{db_scheme}://{db_credentials}@{db_route}"

    def tracking_url(self, tracking_id) -> str:
        return f"{self.DOMAIN}/track/{tracking_id}"

# Instantiate settings
settings = Settings()
