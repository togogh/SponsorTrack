from sponsortrack.backend.connectors.nordvpn_connector import NordVPNConnector
from sponsortrack.backend.connectors.base_connector import BaseConnector
from sponsortrack.config import NORD_VPN_DIRECTORY
import os
import pytest


class TestConnectors:
    @pytest.mark.skipif(
        NORD_VPN_DIRECTORY == "" or NORD_VPN_DIRECTORY is None,
        reason="System does not have NordVPN",
    )
    def test_nord_vpn_connector(self):
        cwd = os.getcwd()
        nord_vpn_connector = NordVPNConnector()

        # Make sure vpn is disconnected just in case it's connected
        nord_vpn_connector.disconnect()

        # Get original IP address
        base_connector = BaseConnector()
        true_cip = base_connector.get_public_ip()

        nord_vpn_connector.connect()
        # Make sure working directory is back to project directory after connecting
        assert os.getcwd() == cwd

        # IP address should have changed after connecting
        assert true_cip != base_connector.get_public_ip()

        nord_vpn_connector.disconnect()
        # Make sure working directory is back to project directory after disconnecting
        assert os.getcwd() == cwd

        # IP address should be back to original after disconnecting
        assert true_cip == base_connector.get_public_ip()
