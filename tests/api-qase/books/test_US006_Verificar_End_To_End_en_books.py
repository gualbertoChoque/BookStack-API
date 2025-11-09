import json

import pytest

from src.common.static_data_modules import StaticDataModules
from src.common.static_headers import StaticDataHeaders
from src.common.static_verbs import StaticDataVerbs
from src.utils.api_calls import request_function
from src.resources.payloads.payloads_shelves.payloads_shelves import (
    create_request_shelves_payload_super_modified
)
from src.common.logger import log_api_call
from config import TOKEN

#Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.e2e_Books
def test_TC001_books(get_url):
        """
        Descripción: Verificar que el todo el flujp de crear, obtener y eliminar un books se lleve de manera correcta y secuencial
        """
        payload = create_request_shelves_payload_super_modified()
        response_post = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value,None,
                                    StaticDataHeaders.default_header.value, json.dumps(payload))
        log_api_call("POST", response_post.url, response_post.headers, payload, TOKEN, response_post)
        assert response_post.status_code == 200
        shelf_id = response_post.json()["id"]
        updated_payload = create_request_shelves_payload_super_modified(
            name="Books_Actualizado",
            description_html="Descripción modificada desde test automatizado"
        )
        response_put = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                   f"{shelf_id}", StaticDataHeaders.default_header.value, json.dumps(updated_payload)
        )
        log_api_call("PUT", response_put.url, response_put.headers, updated_payload, TOKEN, response_put)
        assert response_put.status_code == 200
        assert response_put.json()["name"] == "Books_Actualizado"

        response_get = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                   f"{shelf_id}", StaticDataHeaders.default_header.value
        )
        log_api_call("GET", response_get.url, response_get.headers, None, TOKEN, response_get)
        assert response_get.status_code == 200
        assert response_get.json()["id"] == shelf_id

        response_delete = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                     f"{shelf_id}", StaticDataHeaders.default_header.value
        )
        log_api_call("DELETE", response_delete.url, response_delete.headers, None, TOKEN, response_delete)
        assert response_delete.status_code in [200, 204]



