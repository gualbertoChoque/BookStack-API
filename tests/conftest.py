import json
import os
import sys


import pytest
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from src.common.static_data_shelves import StaticDataProject
from src.resources.payloads.payloads_shelves.payloads_shelves import create_request_shelves_payload_super_modified

from src.headers.headers import generate_headers

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import *
from src.common.static_data_modules import StaticDataModules
from src.common.static_headers import StaticDataHeaders
from src.common.static_verbs import StaticDataVerbs
from src.headers.headers import *
from src.utils.api_calls import request_function
from src.common.logger import log_api_call
from src.assertions.global_assertions import assert_response_schema, assert_response_status_code_global

@pytest.fixture(scope='session')
def get_url():
    return BASE_URI

@pytest.fixture(scope='session')
def get_invalid_url():
    return BASE_INVALID_URI

@pytest.fixture(scope='session')
def get_token():
    return TOKEN

@pytest.fixture(scope="function")
def setup_delete_shelves_by_id(get_url):
    shelves_id_to_delete = None
    def registrar_id(shelves_id):
        nonlocal shelves_id_to_delete
        shelves_id_to_delete = shelves_id

    yield registrar_id
    if shelves_id_to_delete:
        response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
                                    str(shelves_id_to_delete), StaticDataHeaders.default_header.value)
        assert response.status_code in [200, 204]


@pytest.fixture(scope="function")
def setup_delete_books_by_id(get_url):
    books_id_to_delete = None
    def registrar_id(books_id):
        nonlocal books_id_to_delete
        books_id_to_delete = books_id

    yield registrar_id
    if books_id_to_delete:
        response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                    str(books_id_to_delete), StaticDataHeaders.default_header.value)
        assert response.status_code in [200, 204]

"""
Setup para agregar shelves
"""


def _add_shelves(get_url, **kwargs):
    payload = create_request_shelves_payload_super_modified(**kwargs)

    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")

    response = request_function(
        StaticDataVerbs.post.value,
        get_url,
        StaticDataModules.shelves.value,
        None,
        generate_headers(StaticDataHeaders.default_header.value),
        payload
    )

    log_api_call(
        method="POST",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=TOKEN,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    return response.json()


def _add_books(get_url, **kwargs):
    payload = create_request_shelves_payload_super_modified(**kwargs)

    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")

    response = request_function(
        StaticDataVerbs.post.value,
        get_url,
        StaticDataModules.books.value,
        None,
        generate_headers(StaticDataHeaders.default_header.value),
        payload
    )

    log_api_call(
        method="POST",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=TOKEN,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    return response.json()


@pytest.fixture(scope="function")
def setup_add_shelves(get_url):
    return _add_shelves(get_url)

@pytest.fixture(scope="function")
def setup_add_books(get_url):
    return _add_books(get_url)


@pytest.fixture(scope="function")
def setup_add_project_2_character(get_url):
    return _add_shelves(get_url, code=2)

@pytest.fixture(scope="function")
def setup_add_project_10_character(get_url):
    return _add_shelves(get_url, code=10)

@pytest.fixture(scope="function")
def setup_add_project_minus(get_url):
    return _add_shelves(get_url, code="casa")
