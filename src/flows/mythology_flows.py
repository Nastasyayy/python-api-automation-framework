from http import HTTPStatus
from typing import Dict

import allure

from src.api.base import CustomAPISession
from src.api.mythology import MythologyAPIClient
from src.utils.assertions import assert_status_code, assert_response_is_list


class MythologyFlow:
    def __init__(self, session: CustomAPISession):
        self.session = session
        self.api = MythologyAPIClient(session)

    @allure.step("Flow: Get Mythology list")
    def get_and_validate_mythology_list(self) -> Dict[str, str]:
        response = self.api.get_mythology_list()
        assert_status_code(response, HTTPStatus.OK)

        response_json = response.json()
        assert_response_is_list(response_json)
        return response_json
