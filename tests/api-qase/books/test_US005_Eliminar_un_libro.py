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
def test_TC001_Eliminar_un_libro_existente_con_id_valido(get_url, setup_add_books):
    id_to_create = setup_add_books["id"]
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)

    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_status_code_global(204, response.status_code)


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC002_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_la_URL_mal_formada(get_url, setup_add_books):
    id_to_create = setup_add_books["id"]

    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.error_books.value,
                                str(id_to_create), StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "delete_shelves_error405.json", "schemas_shelves")
    assert_response_status_code_global(405, response.status_code)


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC003_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_token_incorrecto(get_url, setup_add_books):
    id_to_create = setup_add_books["id"]

    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                str(id_to_create), StaticDataHeaders.invalid_token_header.value)
    log_api_call(method="DELETE",
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
def test_TC004_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_id_inexistente(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_no_exist_id.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC005_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_id_vacío(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_null.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 403
    assert "Forbidden" in response.text or "permission" in response.text


# Alta
@pytest.mark.regression
@pytest.mark.negative
def test_TC006_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_caracteres_especiales_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_code_param_special.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC007_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_letras_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_string.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC008_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_letras_minusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_minus.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC009_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_letras_mayusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_mayus.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 pero da un 204 ya que toma los valores numericos del ID e ignora los alfabeticos siendo que es un solo ID")
@pytest.mark.regression
@pytest.mark.negative
def test_TC010_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_letras_y_numeros_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_mix.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC011_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_letras_y_numeros_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_cero.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC012_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_varios_0_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_more_cero.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC013_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_valor_negativo_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_negative.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe un libro con id con espacio en el centro")
@pytest.mark.regression
@pytest.mark.negative
def test_TC014_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_espacio_entre_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_space_medium.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error404_by_id.json", "schemas_shelves")
    assert_response_status_code_global(404, response.status_code)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe un libro con el id con espacio por delante")
@pytest.mark.regression
@pytest.mark.negative
def test_TC015_Verificar_que_se_muestre_error_al_eliminar_un_libro_con_espacio_entre_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.invalid_id_param_space.value,
                                StaticDataHeaders.default_header.value)
    log_api_call(method="DELETE",
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
def test_TC016_Verificar_que_un_libro_sin_header_token_devuelva_error(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_token_header.value)

    log_api_call(method="DELETE",
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
def test_TC017_Verificar_que_al_actualizar_un_libro_sin_header_devuelva_error(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_content_header.value)

    log_api_call(method="DELETE",
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
def test_TC018_Verificar_que_un_libro_devuelva_error_405_si_se_usa_método_POST_en_lugar_de_DELETE(get_url):
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.valid_id.value, StaticDataHeaders.default_header.value)

    log_api_call(method="DELETE",
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
def test_TC019_Verificar_que_un_libro_devuelva_error_405_si_se_usa_método_GET_en_lugar_de_DELETE(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.books.value,
                                StaticDataShelvesPorId.valid_param_id.value, StaticDataHeaders.default_header.value)

    log_api_call(method="DELETE",
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
def test_TC020_Actualizar__un_libro_sin_autentificarse(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.books.value,
                                StaticDataHeaders.no_token_header.value)

    log_api_call(method="DELETE",
                 url=response.url,
                 headers=response.headers,
                 payload=None,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)
