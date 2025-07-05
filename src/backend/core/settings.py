from dataclasses import dataclass
from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict
from ipaddress import IPv4Address
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
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    SERVER_IP_ADDRESS: IPv4Address
    SERVER_PORT: int
    SSH_USERNAME: str
    SSH_PKEY_PATH: FilePath


class EmailSettings(BaseSettingsFromEnv):
    RESEND_API_KEY: str
    EMAIL_DOMAIN: str


class WSSettings(BaseSettingsFromEnv):
    WS_PROXY_UN: str
    WS_PROXY_PW: str


class GeneratorSettings(BaseSettingsFromEnv):
    GENERATOR: Generator
    HF_TOKEN: str
    PROVIDER: str
    MODEL: str


project_settings = ProjectSettings()
db_settings = DBSettings()
email_settings = EmailSettings()
ws_settings = WSSettings()
generator_settings = GeneratorSettings()
