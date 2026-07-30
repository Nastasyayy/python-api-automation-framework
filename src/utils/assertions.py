import allure
from http import HTTPStatus
from typing import Any, Dict


@allure.step("Assert response status code is {expected_status}")
def assert_status_code(response: Any, expected_status: HTTPStatus) -> None:
    """Verifies that the HTTP response status code matches the expected value."""
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status.value} ({expected_status.name}), "
        f"but received {response.status_code}. "
        f"Response body: {response.text}"
    )


@allure.step("Assert response body is a JSON array (list)")
def assert_response_is_list(response_json: Any) -> None:
    """Verifies that the parsed JSON response payload is a Python list."""
    assert isinstance(response_json, list), (
        f"Expected the response body to be a JSON array (list), "
        f"but got type: {type(response_json).__name__}"
    )


@allure.step("Assert dictionary contains key: '{key}'")
def assert_key_in_dict(target_dict: Dict[str, Any], key: str) -> None:
    """Universal helper to verify if a specific key exists in a dictionary."""
    assert key in target_dict, (
        f"Expected key '{key}' was not found in the dictionary. "
        f"Available keys: {list(target_dict.keys())}"
    )


@allure.step("Assert value is not empty for: '{value_name}'")
def assert_not_empty(value: Any, value_name: str) -> None:
    """Universal helper to verify that a value (string, list, dict) is not empty/null."""
    assert (
        value
    ), f"Validation failed: '{value_name}' is empty, null, or evaluated to False"


@allure.step("Assert response header content-type contains 'application/json'")
def assert_json_content_type(response: Any) -> None:
    """Verifies that the server returns a JSON content-type header."""
    content_type = response.headers.get("content-type", "")
    assert (
        "application/json" in content_type
    ), f"Expected content-type to contain 'application/json', got '{content_type}'"


@allure.step("Parse and validate GraphQL response structure")
def read_graphql_data(response: Any) -> Dict[str, Any]:
    """Helper to parse GraphQL body, check for errors, and extract data."""
    body = response.json()

    assert (
        "errors" not in body
    ), f"GraphQL payload returned internal errors: {body.get('errors')}"
    assert (
        "data" in body
    ), f"GraphQL response structure is missing the 'data' field: {body}"

    if not body["data"]:
        raise ValueError(f"GraphQL data block is null or empty: {body}")

    return body["data"]


@allure.step("Assert '{object_name}' value is equal to expected one")
def assert_values_are_equal(actual_value, expected_value, object_name):
    assert (
        actual_value == expected_value
    ), f"Expected '{object_name}' value is equal to expected, but it is not."
