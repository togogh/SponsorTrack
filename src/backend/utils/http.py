import requests
from requests.adapters import HTTPAdapter, Retry
from backend.core.settings import ws_settings


def get_requests_session() -> requests.Session:
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s.mount("http://", HTTPAdapter(max_retries=retries))
    if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
        proxy_str = f"http://{ws_settings.WS_PROXY_UN}:{ws_settings.WS_PROXY_PW}@p.webshare.io:80/"
        proxies = {"http": proxy_str}
        s.proxies.update(proxies)
    return s
