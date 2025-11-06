import json

import pytest

from config import BASE_URI, TOKEN
from src.common.logger import log_api_call
from src.common.static_data_modules import StaticDataModules
from src.common.static_data_shelves import StaticDataShelvesPorId
from src.common.static_headers import StaticDataHeaders
from src.common.static_verbs import StaticDataVerbs
from src.utils.api_calls import request_function
from src.assertions.global_assertions import assert_response_schema, assert_response_status_code_global

from src.resources.payloads.payloads_shelves.payloads_shelves import (
    create_request_shelves_payload,
    create_request_shelves_payload_sin_nombre,
    create_request_shelves_imagen_super_modified,
    create_request_shelves_payload_sin_descripcion,
    create_request_shelves_payload_super_modified
)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC001_Actualizar_un_shelves_existente_con_datos_validos(get_url, get_token, setup_add_shelves,
                                                                   setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]

    payload = create_request_shelves_payload_super_modified(name="Estante_Actualizado",
                                                            description_html="Descripción actualizada desde test automatizado"
                                                            )
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    assert "Descripción actualizada" in response.json()[
        "description_html"], "La descripción no se actualizó correctamente"
    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC002_Verificar_que_de_error_al_enviar_una_URL_mal_formada_al_actualizar(get_invalid_url, get_token,
                                                                                    setup_add_shelves,
                                                                                    setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.put.value, get_invalid_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "post_shelves_error405.json", "schemas_shelves")
    assert_response_status_code_global(405, response.status_code)

    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC003_Actualizar_un_shelves_con_los_mismos_nombre(get_url, get_token, setup_add_shelves,
                                                             setup_delete_shelves_by_id):
    shelf_creado = setup_add_shelves
    id_to_update = shelf_creado["id"]

    payload = create_request_shelves_payload_super_modified(name=shelf_creado["name"])

    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC004_Verificar_que_permita_actualizar_un_shelves_con_un_body_basio(get_url, get_token, setup_add_shelves,
                                                                               setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = {}
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.no_content_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC005_Verificar_que_no_permita_crear_un_shelves_con_un_token_incorrecto(get_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.invalid_token_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC006_Verificar_que_no_permita_actualizar_un_shelves_con_un_token_incorrecto(get_url, get_token,
                                                                                        setup_add_shelves,
                                                                                        setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]

    payload = create_request_shelves_payload_super_modified()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.invalid_token_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC007_Verificar_que_no_permita_crear_un_shelves_sin_autentificar(get_url, get_token, setup_add_shelves,
                                                                            setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]

    payload = create_request_shelves_payload_super_modified()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.no_token_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "get_shelves_error401_by_id.json", "schemas_shelves")
    assert_response_status_code_global(401, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC008_Verificar_actualizar_shelves_sin_description(get_url, get_token, setup_add_shelves,
                                                              setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC009_Actualizar_un_shelves_con_nombre_nuevo_en_mayusculas(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="PRUEBA")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC010_Actualizar_un_shelves_con_nombre_nuevo_en_minusculas(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="pruebas")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC011_Actualizar_un_shelves_con_nombre_nuevo_numerico(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="12345")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC012_Actualizar_un_shelves_con_nombre_nuevo_con_caracteres_especiales(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="%$#@&$")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC013_Actualizar_un_shelves_con_nombre_con_espacio_en_medio(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion("Act ualizado")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC014_Actualizar_un_shelves_con_nombre_con_espacio_al_inicio(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion("   Actualizado")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC015_Actualizar_un_shelves_con_nombre_con_espacio_al_final(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion("Actualizado2    ")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un estante con nombre de espacios")
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC016_Verificar_que_no_permita_actualizar_un_shelves_con_solo_espacios(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(name="    ")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC017_Actualizar_un_shelves_con_nombre_alfa_numerico_mixto(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="Shelf123Mix")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Alta
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un estante sin nombre")
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC018_Verificar_que_no_permita_actualizar_un_shelves_con_nombre_nulo(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(name="")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC019_Verificar_actualizar_de_un_shelves_con_nombre_de_1_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=1)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC020_Verificar_actualizar_de_un_shelves_con_nombre_de_2_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=2)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC021_Verificar_actualizar_de_un_shelves_con_nombre_de_254_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=254)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC022_Verificar_actualizar_de_un_shelves_con_nombre_de_255_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=225)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC023_Verificar_actualizar_de_un_shelves_con_nombre_de_125_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=125)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC024_Verificar_actualizar_de_un_shelves_con_nombre_de_256_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=256)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC025_Verificar_actualizar_de_un_shelves_con_nombre_de_280_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=280)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC026_Verificar_la_actualizacion_de_un_shelves_con_imagen(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_imagen_super_modified(image_name="alimentos.jpeg")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un estante sin nombre y sin descripcion")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC027_Verificar_que_no_permita_actualizar_un_shelves_con_con_todos_los_campos_vacíos(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(name="", description_html="")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC028_Verificar_actualizar_de_un_shelves_con_descripcion_de_1_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(description_html=1)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC029_Verificar_actualizar_de_un_shelves_con_descripcion_de_256_solo_carácter(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(description_html=256)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC030_Verificar_actualizar_de_un_shelves_con_espacios_en_descripcion(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(description_html="         ")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_GCTC031_Verificar_actualizar_de_un_shelves_con_descripcion_basio(get_url, get_token, setup_add_shelves,
                                                                      setup_delete_shelves_by_id):
    id_to_update = setup_add_shelves["id"]
    payload = create_request_shelves_payload_super_modified(description_html="")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.shelves.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_shelves_by_id(id_to_update)