import requests


class CustomAPISession(requests.Session):
    """A custom requests Session that automatically prefixes relative URLs with the base API URL."""

    def __init__(self, base_url: str):
        super().__init__()
        # Remove any trailing slashes to avoid double slashes during concatenation
        self.base_url = base_url.rstrip("/")

    def request(self, method, url, *args, **kwargs):
        # If the URL is relative (doesn't start with http/https), prepend the base URL and api path
        if not url.startswith(("http://", "https://")):
            url = f"{self.base_url}/api/{url.lstrip('/')}"
        return super().request(method, url, *args, **kwargs)
