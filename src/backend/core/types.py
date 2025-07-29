from enum import Enum


class Generator(Enum):
    HF = "HF"
    OR = "OR"
    NONE = None


class DeployEnv(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"
