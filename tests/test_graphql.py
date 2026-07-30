import time
from typing import Literal

import allure
import pytest
from src.api.graphql import (
    SoulSummary,
)
from src.utils.assertions import (
    assert_key_in_dict,
    assert_not_empty,
    assert_values_are_equal,
)


@pytest.mark.graphql
@allure.feature("GraphQL API")
@allure.story("Public Soul Retrieval Queries")
def test_graphql_public_queries_return_soul_data(gq_soul_flow):
    """
    Verify that any anonymous client can query allSouls lists and read soul details.
    """

    souls_list = gq_soul_flow.get_and_validate_public_souls_list(limit=3)

    first_soul: SoulSummary = souls_list[0]
    keys: list[Literal["id", "name"]] = ["id", "name"]

    for key_value in keys:
        assert_key_in_dict(first_soul, key_value)
        assert_not_empty(first_soul[key_value].strip(), key_value)

    gq_soul_flow.get_and_validate_soul_details(first_soul["id"])


@pytest.mark.graphql
@allure.feature("GraphQL API")
@allure.story("Scribe Identity Lifecycle")
def test_graphql_scribe_session_flows_work_together(
    gq_soul_flow, scribe_session
):
    """
    Verify registration, authentication, and token verification queries for scribes.
    """

    current_scribe_username = gq_soul_flow.get_and_validate_current_scribe()

    assert_values_are_equal(
        current_scribe_username,
        scribe_session.scribe_credentials["username"],
        "username",
    )


@pytest.mark.graphql
@allure.feature("GraphQL API")
@allure.story("Authenticated Soul Complete Lifecycle")
def test_graphql_authenticated_soul_lifecycle(gq_soul_flow):
    """
    Verify creating, amending, and banishing souls as an authorized scribe.
    """

    timestamp = int(time.time() * 1000)
    soul_name = f"Pytest Soul {timestamp}"
    deed_description = f"Documented in Pytest {timestamp}"

    soul_id = None

    try:
        created_soul = gq_soul_flow.create_and_validate_soul(soul_name)
        soul_id = created_soul["id"]

        gq_soul_flow.patch_and_validate_soul_deeds(soul_id, deed_description)

    finally:
        # Guarantees cleanup even if previous assertions fail
        if soul_id:
            gq_soul_flow.banish_and_validate_soul(soul_id)
