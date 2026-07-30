from http import HTTPStatus
from typing import Dict

import allure

from src.api.auth import (
    create_unique_credentials,
    AuthAPIClient,
)
from src.api.base import CustomAPISession
from src.api.constants import AuthResponseMessage
from src.utils.assertions import (
    assert_status_code,
    assert_key_in_dict,
    assert_values_are_equal,
    assert_not_empty,
)


class AuthFlow:
    def __init__(self, session: CustomAPISession):
        self.session = session
        self.api = AuthAPIClient(session)

    @allure.step("Flow: Register a new user")
    def register_user(self) -> Dict[str, str]:
        """
        Reusable business flow to create a soul through API and verify its initial state.
        Returns the created soul credentials.
        """

        key = "message"
        credentials = create_unique_credentials()

        response = self.api.register_user(credentials)
        assert_status_code(response, HTTPStatus.CREATED)

        response_json = response.json()
        assert_key_in_dict(response_json, key)
        assert_values_are_equal(
            response_json.get(key),
            AuthResponseMessage.SIGNUP_SUCCESS,
            key,
        )
        return credentials

    @allure.step(
        "Flow: Register a new user with a registered user's credentials"
    )
    def register_existing_user(self, credentials) -> None:
        """
        Attempt to register a user with already taken credentials and verify the error.
        """

        key = "error"
        response_uns = self.api.register_user(credentials)
        assert_status_code(response_uns, HTTPStatus.BAD_REQUEST)
        response_uns_json = response_uns.json()

        assert_key_in_dict(response_uns_json, key)
        assert_values_are_equal(
            response_uns_json.get(key),
            AuthResponseMessage.SIGNUP_ERROR,
            key,
        )

    @allure.step("Flow: Authenticate user and extract token")
    def login_user(self, credentials) -> str:
        """
        Reusable business flow to log in a user through API and return the auth token.
        """

        key = "token"

        response = self.api.login_user(credentials)
        assert_status_code(response, HTTPStatus.OK)

        response_json = response.json()
        assert_key_in_dict(response_json, key)

        token_value = response_json.get(key)
        assert_not_empty(token_value, value_name=key)

        return token_value
