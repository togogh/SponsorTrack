from sponsortrack.backend.core.types import Generator
import os
from dataclasses import dataclass
from pydantic import FilePath, PostgresDsn
from ipaddress import IPv4Address
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@dataclass
class Settings:
    PROJECT_NAME: str = "SponsorTrack"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_SCHEMA: str = os.getenv("POSTGRES_SCHEMA")
    DATABASE_URL: PostgresDsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SERVER_IP_ADDRESS: IPv4Address = os.getenv("SERVER_IP_ADDRESS")
    SERVER_PORT: int = os.getenv("SERVER_PORT")
    SSH_USERNAME: str = os.getenv("SSH_USERNAME")
    SSH_PKEY_PATH: FilePath = os.getenv("SSH_PKEY_PATH")

    GENERATOR: Generator = "hf"


settings = Settings()
