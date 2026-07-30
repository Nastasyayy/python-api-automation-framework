import allure
from http import HTTPStatus
from typing import Dict, Any
from src.api.base import CustomAPISession
from src.api.graphql import (
    create_soul,
    banish_soul,
    patch_soul_deeds,
    get_soul,
    SoulDetails,
    get_all_souls,
    SoulSummary,
    get_current_scribe,
)
from src.utils.assertions import (
    assert_status_code,
    assert_key_in_dict,
    read_graphql_data,
    assert_not_empty,
    assert_values_are_equal,
)


class SoulFlows:
    """
    Класс для бизнес-цепочек (flows) работы с сущностью Soul через GraphQL.
    """

    def __init__(self, session: CustomAPISession):
        self.session = session

    @staticmethod
    def _execute_and_validate_graphql(response, root_key: str) -> Any:
        assert_status_code(response, HTTPStatus.OK)
        data = read_graphql_data(response)
        assert_key_in_dict(data, root_key)
        return data[root_key]

    @allure.step("Flow: Create and validate a new soul '{soul_name}'")
    def create_and_validate_soul(
        self, soul_name: str, weight: int = 50
    ) -> Dict[str, Any]:
        """
        Reusable business flow to create a soul through GraphQL and verify its initial state.
        Returns the created soul dictionary containing 'id', 'name', 'status', etc.
        """

        response = create_soul(
            self.session, soul_input={"name": soul_name, "weight": weight}
        )
        created_soul = self._execute_and_validate_graphql(
            response, "createSoul"
        )

        assert_key_in_dict(created_soul, "id")
        assert (
            created_soul["name"] == soul_name
        ), f"Expected name {soul_name}, got {created_soul['name']}"
        # assert "DEAD" in created_soul["status"], f"Expected status to contain 'DEAD', got {created_soul['status']}"

        return created_soul

    @allure.step("Flow: Amend soul deeds with description: '{deed}'")
    def patch_and_validate_soul_deeds(
        self, soul_id: str, deed: str
    ) -> Dict[str, Any]:
        """
        Reusable business flow to add a deed to a soul and verify it was added successfully.
        """

        response = patch_soul_deeds(self.session, id_str=soul_id, deed=deed)

        patched_soul = self._execute_and_validate_graphql(
            response, "patchSoulDeeds"
        )

        assert deed in patched_soul["deeds"], (
            f"Expected deed '{deed}' to be present in soul deeds list, "
            f"but got: {patched_soul['deeds']}"
        )

        return patched_soul

    @allure.step("Flow: Banish and validate cleanup for soul ID: {soul_id}")
    def banish_and_validate_soul(self, soul_id: str) -> None:
        """
        Reusable business flow to delete/banish a soul and verify it was cleaned up successfully.
        """

        response = banish_soul(self.session, id_str=soul_id)

        banished_soul = self._execute_and_validate_graphql(
            response, "banishSoul"
        )

        assert (
            "поглощена амит" in banished_soul.lower()
        ), f"Expected cleanup confirmation, but received: {banished_soul}"

    @allure.step("Flow: Get and validate public souls list (limit={limit})")
    def get_and_validate_public_souls_list(
        self, limit: int
    ) -> list[SoulSummary]:
        """
        Reusable business flow to query allSouls list and verify basic structure.
        """

        response = get_all_souls(self.session, limit=limit)

        all_souls = self._execute_and_validate_graphql(response, "allSouls")

        assert (
            len(all_souls) > 0
        ), "Expected GraphQL allSouls query to return at least one entity"
        return all_souls

    @allure.step("Flow: Get and validate detailed data for soul ID: {soul_id}")
    def get_and_validate_soul_details(self, soul_id: str) -> SoulDetails:
        """
        Reusable business flow to query getSoul by ID and verify full detailed schema.
        """

        allure.attach(
            body=soul_id,
            name="Requested Soul ID",
            attachment_type=allure.attachment_type.TEXT,
        )

        response = get_soul(self.session, soul_id)

        soul_details: SoulDetails = self._execute_and_validate_graphql(
            response, "getSoul"
        )

        assert_values_are_equal(soul_details["id"], soul_id, "id")
        assert_not_empty(soul_details["name"].strip(), "name")

        assert_not_empty(soul_details["status"].strip(), "status")

        assert isinstance(
            soul_details["deeds"], list
        ), "Expected 'deeds' field to be an array list"

        return soul_details

    @allure.step("Flow: Verify and validate current scribe identity")
    def get_and_validate_current_scribe(self) -> str:
        """
        Reusable business flow to query currentScribe and verify the response structure.
        Returns the authenticated scribe's username string.
        """

        response = get_current_scribe(self.session)

        current_scribe = self._execute_and_validate_graphql(
            response, "currentScribe"
        )

        return current_scribe
