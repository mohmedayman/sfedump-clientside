import requests
from urllib.parse import urljoin


class API(requests.Session):
    def __init__(self):
        super().__init__()
        self.base_url = "https://khantarish.com"
        #self.base_url = "http://localhost:5050"

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, "/api/v1"+url)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            **kwargs.pop("headers", {})
        }
        timeout = kwargs.pop("timeout", 350)
        return super().request(method, joined_url, headers=headers, timeout=timeout, *args, **kwargs)
