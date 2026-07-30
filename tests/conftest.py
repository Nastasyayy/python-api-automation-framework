import pytest

from src.api.base import CustomAPISession
from src.api.graphql import create_scribe_session
from src.config.env import env
from src.flows.auth_flows import AuthFlow
from src.flows.mythology_flows import MythologyFlow
from src.flows.soul_flows import SoulFlows


@pytest.fixture(scope="session")
def api_session():
    return CustomAPISession(env.base_url)


@pytest.fixture
def scribe_session(api_session: CustomAPISession) -> CustomAPISession:
    """
    Fixture that provides a fully authenticated GraphQL scribe session.
    It injects the Bearer JWT token directly into headers for automated routing.
    """
    auth_data = create_scribe_session(api_session)

    api_session.headers.update(
        {"Authorization": f"Bearer {auth_data['token']}"}
    )

    api_session.scribe_credentials = auth_data["credentials"]

    return api_session


@pytest.fixture
def gq_soul_flow(scribe_session):
    return SoulFlows(scribe_session)


@pytest.fixture
def auth_flow(api_session):
    return AuthFlow(api_session)


@pytest.fixture
def mythology_flow(api_session):
    return MythologyFlow(api_session)
