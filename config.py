from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self
from pydantic import model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore"
    )

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str 
    SENDER_EMAIL: str
    CONTANT_URL: str

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

# Instantiate settings
settings = Settings()
