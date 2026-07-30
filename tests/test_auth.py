import allure
from src.api.auth import (
    get_configured_credentials,
)


@allure.feature("Authentication API")
@allure.story("User Signup")
@allure.severity(allure.severity_level.BLOCKER)
def test_signup_user_success(auth_flow):
    """Verify that a user sign up in successfully."""

    auth_flow.register_user()


@allure.feature("Authentication API")
@allure.story("User Login")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_user_success(auth_flow):
    """
    Verify that a configured user can log in successfully and receive an auth token.
    """

    credentials = get_configured_credentials()

    auth_flow.login_user(credentials)


@allure.feature("Authentication API")
@allure.story("Duplicate User Signup")
@allure.severity(allure.severity_level.BLOCKER)
def test_signup_user_unsuccessful(auth_flow):
    """
    Verify that a user signup fails if credentials are already taken.
    """

    credentials = auth_flow.register_user()

    auth_flow.register_existing_user(credentials)
