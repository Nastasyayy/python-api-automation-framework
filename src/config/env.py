import os
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()


def _read_optional(name: str) -> str | None:
    value = os.getenv(name)
    if value is not None:
        value = value.strip()
    return value if value else None


env = SimpleNamespace(
    base_url=_read_optional("BASE_URL"),
    graphql_url=_read_optional("GRAPHQL_URL"),
    ui_base_url=_read_optional("UI_BASE_URL"),
    username=_read_optional("USERNAME"),
    password=_read_optional("PASSWORD"),
)
