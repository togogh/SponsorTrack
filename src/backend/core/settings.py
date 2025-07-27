from dataclasses import dataclass
from pydantic import FilePath, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict
from backend.core.types import Generator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


class BaseSettingsFromEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@dataclass
class ProjectSettings:
    NAME: str = "SponsorTrack"
    VERSION: str = "1.0.0"


class DBSettings(BaseSettingsFromEnv):
    POSTGRES_USER: str  # Postgres username
    POSTGRES_PASSWORD: str  # Postgres password
    POSTGRES_SERVER: str  # Postgres server/host
    POSTGRES_REMOTE_PORT: int | None  # Postgres port in server/host
    POSTGRES_LOCAL_PORT: int  # Local postgres port
    POSTGRES_DB: str  # Postgres database name
    POSTGRES_SCHEMA: str  # Postgres schema name
    SERVER_IP_ADDRESS: IPvAnyAddress | None  # IP address of server containing postgres db
    SSH_USERNAME: str | None  # Username to use to ssh into the server
    SSH_PKEY_PATH: FilePath | None  # Path containing ssh private key


# class EmailSettings(BaseSettingsFromEnv):
#     RESEND_API_KEY: str
#     EMAIL_DOMAIN: str


class WSSettings(BaseSettingsFromEnv):
    WS_PROXY_UN: str | None  # Webshare proxy username
    WS_PROXY_PW: str | None  # Webshare proxy password


class GeneratorSettings(BaseSettingsFromEnv):
    GENERATOR: Generator  # Generator type
    HF_TOKEN: str | None  # Huggingface token (required if GENERATOR = 'HF')
    OR_TOKEN: str | None  # OpenRouter token (required if GENERATOR = 'OR')
    PROVIDER: str | None  # Model provider
    MODEL: str  # Model name


project_settings = ProjectSettings()
db_settings = DBSettings()
# email_settings = EmailSettings()
ws_settings = WSSettings()
generator_settings = GeneratorSettings()
