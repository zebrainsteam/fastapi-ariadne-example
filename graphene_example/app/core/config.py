import secrets
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings
from pydantic.class_validators import validator
from pydantic.networks import PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_NAME: Optional[str]
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]
    DEBUG: bool

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError()

    PROJECT_NAME: str = "TODO APP"

    class Config:
        env_file = ".env"


settings = Settings()
