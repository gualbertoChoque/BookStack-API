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
def test_TC001_Obtener_un_libro_existente_con_id_valido(get_url, setup_add_books, setup_delete_books_by_id):
    id_to_create = setup_add_books["id"]
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC002_Obtener_libro_con_header_valido(get_url, setup_add_books, setup_delete_books_by_id):
    id_to_create = setup_add_books["id"]
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC003_Obtener_libros_despues_de_creacion(get_url, setup_add_books, setup_delete_books_by_id):
    id_to_create = setup_add_books["id"]
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC004_Obtener_libro_con_token_valido(get_url, setup_add_books, setup_delete_books_by_id):
    id_to_create = setup_add_books["id"]
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC005_Verificar_que_se_muestre_error_al_mandar_la_URL_mal_formada(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.error_books.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 404
    assert "Page Not Found" in response.text


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC006_Obtener_un_libro_token_incorrecto(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.invalid_token_header.value)

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
def test_TC007_Obtener_un_libros_inexistente(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_no_exist_id.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC008_Verificar_que_no_permita_obtener_un_libros_con_id_vacío(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_null.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 403
    assert "Forbidden" in response.text or "permission" in response.text


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC009_Verificar_que_no_permita_obtener_uns_books_con_caracteres_especiales_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_code_param_special.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC010_Verificar_que_no_permita_obtener_un_libros_con_letras_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_string.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC011_Verificar_que_no_permita_obtener_un_libro_con_letras_minusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_minus.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC012_Verificar_que_no_permita_obtener_un_libro_con_letras_mayusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_mayus.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 Pero el API recooce el primer valor numerico ignorando los alfabeticos")
@pytest.mark.regression
@pytest.mark.negative
def test_TC013_Verificar_que_no_permita_obtener_un_libro_con_letras_y_numeros_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_mix.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC014_Verificar_que_no_permita_obtener_un_libros_con_un_0_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_cero.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC015_Verificar_que_no_permita_obtener_un_libros_con_varios_0_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_more_cero.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC016_Verificar_que_no_permita_obtener_un_libro_con_valor_negativo_en_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_negative.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe en id con espacio en el centro")
@pytest.mark.regression
@pytest.mark.negative
def test_TC017_Verificar_que_no_permita_obtener_un_libros_con_espacio_entre_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_space_medium.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe en id con espacio en el centro")
@pytest.mark.regression
@pytest.mark.negative
def test_TC018_Verificar_que_no_permita_obtener_un_libro_con_espacio_delante_el_id(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_space.value,
                                StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC019_Verificar_que_sin_header_token_devuelva_error_en_libros(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_token_header.value)

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
def test_TC020_Verificar_que_sin_header_devuelva_error_en_libros(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_content_header.value)

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
def test_TC021_Verificar_que_se_devuelva_error_405_si_se_usa_método_POST_en_lugar_de_GET_en_libros(get_url):
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.valid_id.value, StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error405_by_id.json", "schemas_shelves")
    assert_response_status_code_global(405, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC022_Verificar_que_se_devuelva_error_405_si_se_usa_método_DELETE_en_lugar_de_GET_en_libros(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.valid_param_id.value, StaticDataHeaders.default_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.regression
@pytest.mark.negative
def test_TC023_Obtener_un_libro_sin_autentificarse(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_token_header.value)

    log_api_call(method="GET",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)
