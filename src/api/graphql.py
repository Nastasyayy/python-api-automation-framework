import random
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypeVar, Union, TypedDict
import requests

from src.api.base import CustomAPISession
from src.config.env import env


GraphqlVariables = TypedDict[str, Any]


class GraphqlError(TypedDict):
    message: str
    path: Optional[List[Union[int, str]]]
    extensions: Optional[Dict[str, Any]]


TData = TypeVar("TData")


class GraphqlResponseBody(TypedDict):
    data: Optional[Any]
    errors: Optional[List[GraphqlError]]


@dataclass
class GraphqlRequestOptions:
    operation_name: str
    query: str
    token: Optional[str] = None
    variables: Optional[GraphqlVariables] = None


class GraphqlScribeCredentials(TypedDict):
    password: str
    username: str


class GraphqlAuthPayload(TypedDict):
    message: str
    token: str


class SoulSummary(TypedDict):
    id: str
    name: str
    weight: int


class SoulDetails(SoulSummary):
    deeds: List[str]
    status: str


class SoulInput(TypedDict):
    name: str
    weight: int


SoulMutationPayload = SoulDetails

SCRIBE_USERNAME_PREFIX = "pw_scribe"


# Helpers


def _create_auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_graphql_body(options: GraphqlRequestOptions) -> Dict[str, Any]:
    return {
        "operationName": options.operation_name,
        "query": options.query,
        "variables": options.variables
        if options.variables is not None
        else None,
    }


def post_graphql(
    session: CustomAPISession, options: GraphqlRequestOptions
) -> requests.Response:
    headers = _create_auth_headers(options.token) if options.token else None

    return session.post(
        url=env.graphql_url,
        json=_create_graphql_body(options),
        headers=headers,
    )


def _create_username_suffix() -> str:
    timestamp = str(int(time.time() * 1000))
    random_part = f"{random.randint(0, 999999):06d}"
    return f"{timestamp}_{random_part}"


def create_unique_scribe_credentials() -> GraphqlScribeCredentials:
    return {
        "username": f"{SCRIBE_USERNAME_PREFIX}_{_create_username_suffix()}",
        "password": "playwright123",
    }


# API request methods (Queries & Mutations)


def get_all_souls(session: CustomAPISession, limit: int) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="AllSouls",
        query="""
          query AllSouls($limit: Int!) {
            allSouls(limit: $limit) {
              id
              name
              weight
            }
          }
        """,
        variables={"limit": limit},
    )
    return post_graphql(session, options)


def get_soul(session: CustomAPISession, id_str: str) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="GetSoul",
        query="""
          query GetSoul($id: ID!) {
            getSoul(id: $id) {
              id
              name
              deeds
              status
              weight
            }
          }
        """,
        variables={"id": id_str},
    )
    return post_graphql(session, options)


def register_scribe(
    session: CustomAPISession, credentials: GraphqlScribeCredentials
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="RegisterScribe",
        query="""
          mutation RegisterScribe($username: String!, $password: String!) {
            registerScribe(username: $username, password: $password)
          }
        """,
        variables=credentials,
    )
    return post_graphql(session, options)


def login_scribe(
    session: CustomAPISession, credentials: GraphqlScribeCredentials
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="LoginScribe",
        query="""
          mutation LoginScribe($username: String!, $password: String!) {
            loginScribe(username: $username, password: $password) {
              token
              message
            }
          }
        """,
        variables=credentials,
    )
    return post_graphql(session, options)


def get_current_scribe(
    session: CustomAPISession, token: str
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="CurrentScribe",
        query="""
          query CurrentScribe {
            currentScribe
          }
        """,
        token=token,
    )
    return post_graphql(session, options)


def create_soul(
    session: CustomAPISession, token: str, soul_input: SoulInput
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="CreateSoul",
        query="""
          mutation CreateSoul($input: SoulInput!) {
            createSoul(input: $input) {
              id
              name
              deeds
              status
              weight
            }
          }
        """,
        token=token,
        variables={"input": soul_input},
    )
    return post_graphql(session, options)


def patch_soul_deeds(
    session: CustomAPISession, token: str, id_str: str, deed: str
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="PatchSoulDeeds",
        query="""
          mutation PatchSoulDeeds($id: ID!, $deed: String!) {
            patchSoulDeeds(id: $id, deed: $deed) {
              id
              name
              deeds
              status
              weight
            }
          }
        """,
        token=token,
        variables={"id": id_str, "deed": deed},
    )
    return post_graphql(session, options)


def banish_soul(
    session: CustomAPISession, token: str, id_str: str
) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="BanishSoul",
        query="""
          mutation BanishSoul($id: ID!) {
            banishSoul(id: $id)
          }
        """,
        token=token,
        variables={"id": id_str},
    )
    return post_graphql(session, options)
