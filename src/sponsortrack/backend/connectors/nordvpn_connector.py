from sponsortrack.config import NORD_VPN_DIRECTORY
import os
import subprocess
from sponsortrack.backend.connectors.base_connector import BaseConnector


class NordVPNConnector(BaseConnector):
    def connect(self):
        if NORD_VPN_DIRECTORY == "" or NORD_VPN_DIRECTORY is None:
            raise ValueError("Path to NordVPN is missing")
        cwd = os.getcwd()
        os.chdir(NORD_VPN_DIRECTORY)
        subprocess.run(["nordvpn", "-c"])
        self.retry_check_ip()
        os.chdir(cwd)

    def disconnect(self):
        if NORD_VPN_DIRECTORY == "" or NORD_VPN_DIRECTORY is None:
            raise ValueError("Path to NordVPN is missing")
        cwd = os.getcwd()
        os.chdir(NORD_VPN_DIRECTORY)
        subprocess.run(["nordvpn", "-d"])
        self.retry_check_ip(connect=False)
        os.chdir(cwd)
