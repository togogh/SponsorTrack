from sponsortrack.config import NORD_VPN_DIRECTORY
import os
import subprocess


class NordVPNConnector:
    def connect(self):
        cwd = os.getcwd()
        os.chdir(NORD_VPN_DIRECTORY)
        subprocess.run(["nordvpn", "-c"])
        os.chdir(cwd)

    def disconnect(self):
        cwd = os.getcwd()
        os.chdir(NORD_VPN_DIRECTORY)
        subprocess.run(["nordvpn", "-d"])
        os.chdir(cwd)
