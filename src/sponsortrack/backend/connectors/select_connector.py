from sponsortrack.config import CONNECTOR
from sponsortrack.backend.connectors.nordvpn_connector import NordVPNConnector


def select_connector():
    match CONNECTOR:
        case "nordvpn":
            return NordVPNConnector()
        case None:
            return None
