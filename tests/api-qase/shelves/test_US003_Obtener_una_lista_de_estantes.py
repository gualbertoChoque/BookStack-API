import pytest

from config import BASE_URI, TOKEN
from src.common.logger import log_api_call
from src.common.static_data_modules import StaticDataModules
from src.common.static_data_shelves import StaticDataShelvesPorId
from src.common.static_headers import StaticDataHeaders
from src.common.static_verbs import StaticDataVerbs
from src.utils.api_calls import request_function
from src.assertions.global_assertions import assert_response_schema, assert_response_status_code_global


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC001_Obtener_la_lista_de_estantes_visibles(get_url):

    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.shelves.value,
                               "", StaticDataHeaders.default_header.value
    )

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_list_shelves_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC002_Verificar_error_al_obtener_una_lista_sin_token(get_url):

    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.shelves.value,
                               "", StaticDataHeaders.no_token_header.value
    )

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)

# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC003_Verificar_error_al_obtener_una_lista_con_token_invalido(get_url):

    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.shelves.value,
                               "", StaticDataHeaders.invalid_token_header.value
    )

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC004_Verificar_error_al_obtener_una_lista_con_la_URL_incorrecta(get_url):

    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.error_shelve.value,
                               "", StaticDataHeaders.default_header.value
    )

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 404
    assert "Page Not Found" in response.text