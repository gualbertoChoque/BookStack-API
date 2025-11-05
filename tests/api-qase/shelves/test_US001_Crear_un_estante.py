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
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC001_Crear_un_shelves_exitoso(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC002_Verificar_que_de_error_al_enviar_una_URL_mal_formada(get_invalid_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_invalid_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error405.json", "schemas_shelves")
    assert_response_status_code_global(405, response.status_code)

# Alta
@pytest.mark.xfail(reason="Deberia devolver un 400 ya que no deberia crearse un estante con el nombre repetido")
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC003_Verificar_que_de_error_Crear_shelves_con_nombre_existente_en_lista(get_url, get_token,
                                                                                        setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="Prueba5")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                    StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                     url=response.url,
                     headers=response.headers,
                     payload=payload,
                     token=TOKEN,
                     response=response
                     )
    assert_response_status_code_global(400, response.status_code)

#Media
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC004_Verificar_que_no_permita_crear_un_shelves_con_un_body_inválido(get_url, get_token,
                                                                                        setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="Prueba5")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                    StaticDataHeaders.no_content_header.value, json.dumps(payload))

    log_api_call(method="POST",
                     url=response.url,
                     headers=response.headers,
                     payload=payload,
                     token=TOKEN,
                     response=response
                     )
    assert_response_status_code_global(422, response.status_code)

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
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC006_Verificar_que_no_permita_crear_un_shelves_sin_autentificar(get_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.no_token_header.value, json.dumps(payload))

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
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC007_Crear_shelves_con_todos_los_campos_disponibles(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])

# Alta
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC008_Verificar_crear_shelves_sin_description(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_sin_descripcion()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC009_Crear_un_shelves_con_nombre_mayusculas(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="PRUEBA")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])

# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC010_Crear_un_shelves_con_nombre_minusculas(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="pruebas")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])

# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC011_Crear_un_shelves_con_nombre_minusculas_y_mayusculas(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC012_Crear_un_shelves_con_nombre_numerico(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="12345")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC013_Crear_un_shelves_con_nombre_con_caracteres_especiales(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="%$#@&$")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC014_Crear_un_shelves_con_nombre_con_espacio_en_medio(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="Pru eba")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC015_Crear_un_shelves_con_nombre_con_espacio_al_inicio(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=" Prueba")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC016_Crear_un_shelves_con_nombre_con_espacio_al_final(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="Espacio  ")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC017_Verificar_que_no_permita_crear_un_shelves_con_solo_espacios(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="    ")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC018_Crear_un_shelves_con_nombre_alfa_numerico_mixto(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name="Shelf123Mix")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC019_Verificar_que_no_permita_crear_un_shelves_con_nombre_nulo(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC020_Verificar_la_creación_de_un_shelves_con_nombre_de_1_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=1)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC021_Verificar_la_creación_de_un_shelves_con_nombre_de_2_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=2)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC022_Verificar_la_creación_de_un_shelves_con_nombre_de_254_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=254)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC023_Verificar_la_creación_de_un_shelves_con_nombre_de_255_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=255)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC024_Verificar_la_creación_de_un_shelves_con_nombre_de_125_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(name=125)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC025_Verificar_la_creación_de_un_shelves_con_nombre_de_256_solo_carácter(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name=256)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC026_Verificar_la_creación_de_un_shelves_con_nombre_de_280_solo_carácter(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name=280)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC027_Verificar_la_creación_de_un_shelves_con_imagen(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="alimentos.jpeg")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC028_Verificar_que_no_permita_crear_un_shelves_con_con_todos_los_campos_vacíos(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="", description_html="")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "post_shelves_error422.json", "schemas_shelves")
    assert_response_status_code_global(422, response.status_code)


# Media
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC029_Verificar_la_creación_de_un_shelves_con_descripcion_de_1_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(description_html=1)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])

# Media
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC030_Verificar_la_creación_de_un_shelves_con_descripcion_de_256_solo_carácter(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(description_html=256)
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC031_Verificar_la_creación_de_un_shelves_con_descripcion_con_espaiosr(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="      ")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])


# Media
@pytest.mark.positive
@pytest.mark.regression
def test_GCTC032_Verificar_la_creación_de_un_shelves_con_descripcion_con_caractesres_especiales_numericos_alfabetico(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="Ca12345@#$%^#@lahsa")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])

#Alta
@pytest.mark.negative
@pytest.mark.regression
def test_GCTC033_Verificar_que_no_permita_crear_un_shelves_con_descripcion_basio(get_url, get_token, setup_delete_shelves_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="")
    assert_response_schema(payload, "add_shelves_schema_request.json", "schemas_shelves")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.shelves.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_shelves_schema_response.json", "schemas_shelves")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    print(f" Shelves creado correctamente → ID: {response.json()['id']} | Nombre: {response.json()['name']}")
    setup_delete_shelves_by_id(response.json()["id"])