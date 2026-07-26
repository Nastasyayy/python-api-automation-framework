import pytest

from src.api.base import CustomAPISession
from src.config.env import env


@pytest.fixture(scope="session")
def api_session():
    return CustomAPISession(env.base_url)
