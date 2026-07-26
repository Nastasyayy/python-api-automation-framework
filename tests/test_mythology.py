import allure
from http import HTTPStatus
from src.api.mythology import get_mythology_list
from src.utils.assertions import assert_status_code, assert_response_is_list


@allure.feature("Mythology API")
@allure.story("Get Mythology List")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_mythology_list_success(api_session):
    """Verify that the mythology endpoint is accessible and returns a 200 OK status code."""

    response = get_mythology_list(api_session)
    assert_status_code(response, HTTPStatus.OK)

    response_json = response.json()
    assert_response_is_list(response_json)
