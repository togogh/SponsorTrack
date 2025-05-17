import time
import requests


class BaseConnector:
    def get_public_ip(self):
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

        raise ConnectionError("Cannot get public ip")

    def retry_check_ip(self, retries=5, connect=True):
        # buffer so that vpn has time to connect/disconnect
        cip = self.get_public_ip()
        desired_ip_same = False if connect else True
        ip_same = cip == self.get_public_ip()
        i = 0
        while i < retries and ip_same != desired_ip_same:
            time.sleep(30)
            ip_same = cip == self.get_public_ip()
            i += 1

    def connect(self):
        pass

    def disconnect(self):
        pass
