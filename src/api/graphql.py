import random
import re
import time
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, List, Optional, TypedDict
import allure
import requests

from src.api.base import CustomAPISession
from src.config.env import env
from src.utils.assertions import (
    assert_json_content_type,
    assert_key_in_dict,
    assert_not_empty,
    assert_status_code,
    read_graphql_data,
)

SCRIBE_USERNAME_PREFIX = "myth_fr_scribe"

# Pattern to validate JWT tokens inside helpers
JWT_PATTERN = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")

# Types and DTOs
GraphqlVariables = Dict[str, Any]


@dataclass
class GraphqlRequestOptions:
    operation_name: str
    query: str
    variables: Optional[GraphqlVariables] = None


class GraphqlScribeCredentials(TypedDict):
    password: str
    username: str


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


class GraphqlScribeSession(TypedDict):
    credentials: GraphqlScribeCredentials
    token: str


# Core GraphQL Helpers


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
    return session.post(
        url=env.graphql_url,
        json=_create_graphql_body(options),
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


def create_scribe_session(session: CustomAPISession) -> GraphqlScribeSession:
    """
    Helper to automate registration and login flow for a unique GraphQL scribe.
    """

    credentials = create_unique_scribe_credentials()

    with allure.step("Register a GraphQL scribe"):
        register_response = register_scribe(session, credentials)
        assert_status_code(register_response, HTTPStatus.OK)
        assert_json_content_type(register_response)

        register_data = read_graphql_data(register_response)
        assert_key_in_dict(register_data, "registerScribe")
        assert_not_empty(
            register_data["registerScribe"].strip(), "registerScribe message"
        )

    with allure.step("Log in as the GraphQL scribe"):
        login_response = login_scribe(session, credentials)
        assert_status_code(login_response, HTTPStatus.OK)
        assert_json_content_type(login_response)

        login_data = read_graphql_data(login_response)
        assert_key_in_dict(login_data, "loginScribe")

        login_payload = login_data["loginScribe"]
        assert_key_in_dict(login_payload, "token")
        assert_key_in_dict(login_payload, "message")

        assert_not_empty(login_payload["message"].strip(), "login message")
        assert JWT_PATTERN.match(
            login_payload["token"]
        ), f"Token '{login_payload['token']}' is not a valid JWT format"

    return {
        "credentials": credentials,
        "token": login_payload["token"],
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


def get_current_scribe(session: CustomAPISession) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="CurrentScribe",
        query="""
          query CurrentScribe {
            currentScribe
          }
        """,
    )
    return post_graphql(session, options)


def create_soul(
    session: CustomAPISession, soul_input: SoulInput
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
        variables={"input": soul_input},
    )
    return post_graphql(session, options)


def patch_soul_deeds(
    session: CustomAPISession, id_str: str, deed: str
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
        variables={"id": id_str, "deed": deed},
    )
    return post_graphql(session, options)


def banish_soul(session: CustomAPISession, id_str: str) -> requests.Response:
    options = GraphqlRequestOptions(
        operation_name="BanishSoul",
        query="""
          mutation BanishSoul($id: ID!) {
            banishSoul(id: $id)
          }
        """,
        variables={"id": id_str},
    )
    return post_graphql(session, options)
