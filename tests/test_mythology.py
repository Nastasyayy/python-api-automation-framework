import allure
from http import HTTPStatus
from src.api.mythology import get_mythology_list


@allure.feature("Mythology API")
@allure.story("Get Mythology List")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_mythology_list_success(api_session):
    """Verify that the mythology endpoint is accessible and returns a 200 OK status code."""

    response = get_mythology_list(api_session)

    assert response.status_code == HTTPStatus.OK, (
        f"Expected status code {HTTPStatus.OK.value}, but received {response.status_code}. "
        f"Response body: {response.text}"
    )

    response_json = response.json()
    assert isinstance(
        response_json, list
    ), "Expected the response body to be a JSON array (list)"

    print(f"\nSuccess! Retrieved {len(response_json)} mythology entities.")
