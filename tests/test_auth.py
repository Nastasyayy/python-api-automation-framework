import allure
from http import HTTPStatus
from src.api.auth import login_user, get_configured_credentials
from src.utils.assertions import (
    assert_status_code,
    assert_key_in_dict,
    assert_not_empty,
)


@allure.feature("Authentication API")
@allure.story("User Login")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_user_success(api_session):
    """Verify that a configured user can login successfully and receive an auth token."""

    key = "token"
    credentials = get_configured_credentials()

    response = login_user(api_session, credentials)
    assert_status_code(response, HTTPStatus.OK)

    response_json = response.json()
    assert_key_in_dict(response_json, key)
    assert_not_empty(response_json.get(key), value_name=key)
