from enum import Enum


class Connector(Enum):
    nordvpn = "nordvpn"
    none = None


class Generator(Enum):
    hf = "hf"
    none = None
