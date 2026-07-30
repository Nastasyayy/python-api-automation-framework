import random
import time
import requests
from typing import TypedDict
from src.config.env import env
from src.api.base import CustomAPISession


class AuthCredentials(TypedDict):
    username: str
    password: str


class RegisterResponseBody(TypedDict):
    message: str


class LoginResponseBody(TypedDict):
    token: str


class AuthSession(TypedDict):
    credentials: AuthCredentials
    token: str


REGISTER_USERNAME_PREFIX = "test_user"
DEFAULT_TEST_PASSWORD = "Test123!"


def _require_env_value(value: str | None, name: str) -> str:
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _create_username_suffix() -> str:
    timestamp = int(time.time() * 1000)
    random_part = f"{random.randint(0, 999999):06d}"
    return f"{timestamp}_{random_part}"


def get_configured_credentials() -> AuthCredentials:
    return {
        "username": _require_env_value(env.username, "USERNAME"),
        "password": _require_env_value(env.password, "PASSWORD"),
    }


def create_unique_credentials(
    password: str = DEFAULT_TEST_PASSWORD,
) -> AuthCredentials:
    return {
        "username": f"{REGISTER_USERNAME_PREFIX}_{_create_username_suffix()}",
        "password": password,
    }


def create_unique_credentials_from_env() -> AuthCredentials:
    password = _require_env_value(env.password, "PASSWORD")
    return create_unique_credentials(password)


class AuthAPIClient:
    def __init__(self, session: CustomAPISession):
        self.session = session

    def register_user(self, credentials: AuthCredentials) -> requests.Response:
        return self.session.post("register", json=credentials)

    def login_user(self, credentials: AuthCredentials) -> requests.Response:
        return self.session.post("login", json=credentials)

    def create_auth_session(self) -> AuthSession:
        credentials = get_configured_credentials()
        login_response = self.login_user(credentials)

        if not login_response.ok:
            raise RuntimeError(
                f"Login failed for configured USERNAME/PASSWORD: "
                f"{login_response.status_code} {login_response.text}"
            )

        body: LoginResponseBody = login_response.json()

        return {
            "credentials": credentials,
            "token": body["token"],
        }
