from typing import Dict, Literal, Optional, TypedDict
import requests
from src.api.base import CustomAPISession

MythologyCategory = Literal["gods", "heroes", "creatures"]
MythologyListCategory = Literal["gods", "heroes", "creatures", "all"]
MythologySortDirection = Literal["asc", "desc"]


# Data structures
class GetMythologyListQueryParams(TypedDict, total=False):
    category: MythologyListCategory
    sort: MythologySortDirection


class MythologyEntity(TypedDict):
    id: int
    name: str
    category: str
    desc: str
    img: Optional[str]


class CreateMythologyPayload(TypedDict):
    name: str
    category: MythologyCategory
    desc: str
    img: Optional[str]


# In Python, total=False is used for Partial types
class PatchMythologyPayload(TypedDict, total=False):
    name: str
    category: MythologyCategory
    desc: str
    img: Optional[str]


UpdateMythologyPayload = CreateMythologyPayload


# Helper functions
def _create_auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# API request methods (REST)
class MythologyAPIClient:
    def __init__(self, session: CustomAPISession):
        self.session = session

    def get_mythology_list(
        self,
        query: Optional[GetMythologyListQueryParams] = None,
    ) -> requests.Response:
        return self.session.get("mythology", params=query)

    def get_mythology_by_id(self, entity_id: int) -> requests.Response:
        return self.session.get(f"mythology/{entity_id}")

    def create_mythology_entity_without_auth(
        self, payload: CreateMythologyPayload
    ) -> requests.Response:
        return self.session.post("mythology", json=payload)

    def create_mythology_entity(
        self, token: str, payload: CreateMythologyPayload
    ) -> requests.Response:
        return self.session.post(
            "mythology", json=payload, headers=_create_auth_headers(token)
        )

    def replace_mythology_entity(
        self,
        token: str,
        entity_id: int,
        payload: UpdateMythologyPayload,
    ) -> requests.Response:
        return self.session.put(
            f"mythology/{entity_id}",
            json=payload,
            headers=_create_auth_headers(token),
        )

    def replace_mythology_entity_without_auth(
        self, entity_id: int, payload: UpdateMythologyPayload
    ) -> requests.Response:
        return self.session.put(f"mythology/{entity_id}", json=payload)

    def patch_mythology_entity(
        self,
        token: str,
        entity_id: int,
        payload: PatchMythologyPayload,
    ) -> requests.Response:
        return self.session.patch(
            f"mythology/{entity_id}",
            json=payload,
            headers=_create_auth_headers(token),
        )

    def patch_mythology_entity_without_auth(
        self, entity_id: int, payload: PatchMythologyPayload
    ) -> requests.Response:
        return self.session.patch(f"mythology/{entity_id}", json=payload)

    def delete_mythology_entity(
        self, token: str, entity_id: int
    ) -> requests.Response:
        return self.session.delete(
            f"mythology/{entity_id}", headers=_create_auth_headers(token)
        )

    def delete_mythology_entity_without_auth(
        self, entity_id: int
    ) -> requests.Response:
        return self.session.delete(f"mythology/{entity_id}")
