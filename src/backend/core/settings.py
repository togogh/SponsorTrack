import os
from dataclasses import dataclass
from pydantic import FilePath
from ipaddress import IPv4Address
from backend.core.types import Generator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


@dataclass
class ProjectSettings:
    NAME: str = "SponsorTrack"
    VERSION: str = "1.0.0"


@dataclass
class DBSettings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_SCHEMA: str = os.getenv("POSTGRES_SCHEMA")
    SERVER_IP_ADDRESS: IPv4Address = os.getenv("SERVER_IP_ADDRESS")
    SERVER_PORT: int = os.getenv("SERVER_PORT")
    SSH_USERNAME: str = os.getenv("SSH_USERNAME")
    SSH_PKEY_PATH: FilePath = os.getenv("SSH_PKEY_PATH")


@dataclass
class EmailSettings:
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    EMAIL_DOMAIN: str = os.getenv("EMAIL_DOMAIN")


@dataclass
class WSSettings:
    WS_PROXY_UN: str = os.getenv("WS_PROXY_UN")
    WS_PROXY_PW: str = os.getenv("WS_PROXY_PW")


@dataclass
class GeneratorSettings:
    GENERATOR: Generator = "HF"
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    PROVIDER: str = "novita"
    MODEL: str = "deepseek-ai/DeepSeek-V3-0324"


project_settings = ProjectSettings()
db_settings = DBSettings()
email_settings = EmailSettings()
ws_settings = WSSettings()
generator_settings = GeneratorSettings()
