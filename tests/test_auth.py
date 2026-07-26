from http import HTTPStatus

from src.api.auth import login_user, get_configured_credentials


def test_login_user_success(api_session):
    """Verify that a configured user can login successfully and receive an auth token."""

    credentials = get_configured_credentials()

    response = login_user(api_session, credentials)

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Login failed: {response.text}"

    response_json = response.json()
    assert (
        "token" in response_json
    ), "Response body must contain an authentication token"
    assert response_json["token"] != "", "Token should not be an empty string"
