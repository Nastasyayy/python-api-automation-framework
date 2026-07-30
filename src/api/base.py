import requests
from typing import Any, Optional, Dict
from src.utils.allure_logger import log_allure_http


class CustomAPISession(requests.Session):
    """A custom requests Session that automatically prefixes relative URLs with the base API URL."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.scribe_credentials: Optional[Dict[str, str]] = None

    def request(
        self, method: str, url: str, *args: Any, **kwargs: Any
    ) -> requests.Response:
        if not url.startswith(("http://", "https://")):
            url = f"{self.base_url}/api/{url.lstrip('/')}"

        return log_allure_http(super().request, method, url, *args, **kwargs)
