import allure


@allure.feature("Mythology API")
@allure.story("Get Mythology List")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_mythology_list_success(mythology_flow):
    """
    Verify that the mythology endpoint is accessible and returns a 200 OK status code.
    """

    mythology_flow.get_and_validate_mythology_list()
