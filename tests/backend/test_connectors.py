from sponsortrack.backend.connectors.nordvpn import NordVPNConnector
import os
import requests
import time


def get_public_ip():
    ip_services = [
        "https://api.ipify.org",
        "https://checkip.amazonaws.com/",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
    ]

    for service in ip_services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except (requests.RequestException, ConnectionError):
            continue

    return None


def retry_check_ip(cip, retries=5, connect=True, i=0):
    # buffer so that vpn has time to connect/disconnect
    desired_ip_same = False if connect else True
    ip_same = cip == get_public_ip()
    while i < retries and ip_same != desired_ip_same:
        time.sleep(30)
        ip_same = cip == get_public_ip()
        i += 1


def test_nord_vpn_connector():
    cwd = os.getcwd()
    cip = get_public_ip()

    # Make sure vpn is disconnected just in case it's connected
    nord_vpn_connector = NordVPNConnector()
    nord_vpn_connector.disconnect()
    retry_check_ip(cip, connect=False)

    # Get non-vpn ip address
    true_cip = get_public_ip()

    nord_vpn_connector.connect()
    # Make sure working directory is back to project directory
    assert os.getcwd() == cwd

    retry_check_ip(true_cip)
    # Ip address should have changed after connecting
    assert true_cip != get_public_ip()

    nord_vpn_connector.disconnect()
    assert os.getcwd() == cwd

    retry_check_ip(true_cip, connect=False)
    # Should be back to non-vpn address after disconnecting
    assert true_cip == get_public_ip()
