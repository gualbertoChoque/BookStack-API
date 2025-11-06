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
def test_GCTC001_Eliminar_un_estante_existente_con_id_valido(get_url, setup_add_shelves):
    id_to_create = setup_add_shelves["id"]
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC002_Verificar_que_se_muestre_error_al_eliminar_con_la_URL_mal_formada(get_url, setup_add_shelves):
    id_to_create = setup_add_shelves["id"]

    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.error_shelve.value,
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
def test_GCTC003_Verificar_que_se_muestre_error_al_eliminar_con_token_incorrecto(get_url, setup_add_shelves):
    id_to_create = setup_add_shelves["id"]

    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC004_Verificar_que_se_muestre_error_al_eliminar_con_id_inexistente(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC005_Verificar_que_se_muestre_error_al_eliminar_con_id_vacío(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC006_Verificar_que_se_muestre_error_al_eliminar_con_caracteres_especiales_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC007_Verificar_que_se_muestre_error_al_eliminar_con_letras_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC008_Verificar_que_se_muestre_error_al_eliminar_con_letras_minusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC009_Verificar_que_se_muestre_error_al_eliminar_con_letras_mayusculas_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
@pytest.mark.regression
@pytest.mark.negative
def test_GCTC010_Verificar_que_se_muestre_error_al_eliminar_con_letras_y_numeros_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC011_Verificar_que_se_muestre_error_al_eliminar_con_letras_y_numeros_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC012_Verificar_que_se_muestre_error_al_eliminar_con_varios_0_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC013_Verificar_que_se_muestre_error_al_eliminar_con_valor_negativo_en_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe en id con espacio en el centro")
@pytest.mark.regression
@pytest.mark.negative
def test_GCTC014_Verificar_que_se_muestre_error_al_eliminar_con_espacio_entre_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
@pytest.mark.xfail(reason="Deberia devolver un 404 ya que no existe en id con espacio por delante")
@pytest.mark.regression
@pytest.mark.negative
def test_GCTC015_Verificar_que_se_muestre_error_al_eliminar_con_espacio_entre_el_id(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC016_Verificar_que_sin_header_token_devuelva_error(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC017_Verificar_que_al_actualizar_sin_header_devuelva_error(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC018_Verificar_que_se_devuelva_error_405_si_se_usa_método_POST_en_lugar_de_DELETE(get_url):
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC019_Verificar_que_se_devuelva_error_405_si_se_usa_método_GET_en_lugar_de_DELETE(get_url):
    response = request_function(StaticDataVerbs.get.value, get_url, StaticDataModules.shelves.value,
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
def test_GCTC020_Actualizar_un_shelves_sin_autentificarse(get_url):
    response = request_function(StaticDataVerbs.delete.value, get_url, StaticDataModules.shelves.value,
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
