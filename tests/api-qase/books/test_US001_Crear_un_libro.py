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
def test_TC001_Crear_un_libro_exitoso(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC002_Verificar_que_de_error_al_enviar_una_URL_mal_formada_en_libros(get_invalid_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_invalid_url, StaticDataModules.books.value, None,
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
@pytest.mark.xfail(reason="Deberia devolver un 400 ya que no deberia crearse un libro con el nombre repetido")
@pytest.mark.negative
@pytest.mark.regression
def test_TC003_Verificar_que_de_error_Crear_libro_con_nombre_existente_en_lista(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="Prueba5")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC004_Verificar_que_no_permita_crear_un_libro_con_un_body_inválido(get_url, get_token,
                                                                                        setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="Prueba5")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC005_Verificar_que_no_permita_crear_un_libro_con_un_token_incorrecto(get_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC006_Verificar_que_no_permita_crear_un_libro_sin_autentificar(get_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC007_Crear_un_libro_con_todos_los_campos_disponibles(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])

# Alta
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC008_Verificar_crear_un_libro_sin_description(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_sin_descripcion()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC009_Crear_un_libro_con_nombre_mayusculas(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="PRUEBA")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])

# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC010_Crear_un_libro_con_nombre_minusculas(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="pruebas")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])

# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC011_Crear_un_libro_con_nombre_minusculas_y_mayusculas(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC012_Crear_un_libro_con_nombre_numerico(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="12345")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC013_Crear_un_libro_con_nombre_con_caracteres_especiales(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="%$#@&$")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC014_Crear_un_shelves_con_nombre_con_espacio_en_medio(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="Pru eba")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC015_Crear_un_libro_con_nombre_con_espacio_al_inicio(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=" Prueba")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC016_Crear_un_libro_con_nombre_con_espacio_al_final(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="Espacio  ")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC017_Verificar_que_no_permita_crear_un_libro_con_solo_espacios(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="    ")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC018_Crear_un_libro_con_nombre_alfa_numerico_mixto(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name="Shelf123Mix")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC019_Verificar_que_no_permita_crear_un_libro_con_nombre_nulo(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC020_Verificar_la_creación_de_un_libro_con_nombre_de_1_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=1)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC021_Verificar_la_creación_de_un_libro_con_nombre_de_2_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=2)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC022_Verificar_la_creación_de_un_libro_con_nombre_de_254_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=254)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC023_Verificar_la_creación_de_un_libro_con_nombre_de_255_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=255)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC024_Verificar_la_creación_de_un_libro_con_nombre_de_125_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(name=125)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC025_Verificar_la_creación_de_un_libros_con_nombre_de_256_solo_carácter(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name=256)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC026_Verificar_la_creación_de_un_libro_con_nombre_de_280_solo_carácter(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name=280)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC027_Verificar_la_creación_de_un_libro_con_imagen(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="alimentos.jpeg")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC028_Verificar_que_no_permita_crear_un_libro_con_con_todos_los_campos_vacíos(get_url, get_token):
    payload = create_request_shelves_payload_super_modified(name="", description_html="")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
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
def test_TC029_Verificar_la_creación_de_un_libro_con_descripcion_de_1_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(description_html=1)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])

# Media
@pytest.mark.positive
@pytest.mark.regression
def test_TC030_Verificar_la_creación_de_un_libro_con_descripcion_de_256_solo_carácter(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(description_html=256)
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.positive
@pytest.mark.regression
def test_TC031_Verificar_la_creación_de_un_libro_con_descripcion_con_espaiosr(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="      ")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.positive
@pytest.mark.regression
def test_TC032_Verificar_la_creación_de_un_libro_con_descripcion_con_caractesres_especiales_numericos_alfabetico(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="Ca12345@#$%^#@lahsa")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])

#Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC033_Verificar_que_no_permita_crear_un_libro_con_descripcion_basio(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_payload_super_modified(description_html="")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC034_Verificar_la_creación_de_un_libro_con_imagen_svg(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="circle-user-regular.svg")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC035_Verificar_la_creación_de_un_libro_con_imagen_en_formato_png(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="logo.png")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(response.json()["id"])


# Media
@pytest.mark.xfail(reason="Deberia devolver un 400 o 404 ya que no deberia aceptar un formato de imagen .pdf en un libro")
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC036_Verificar_error_de_un_libro_con_imagen_en_formato_pdf(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="Bug Advocacy.pdf")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 404
    assert "Page Not Found" in response.text


# Media
@pytest.mark.xfail(reason="Deberia devolver un 400 o 404 ya que no deberia aceptar un formato de imagen .gif en un libro")
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC037_Verificar_error_de_un_libro_con_imagen_en_formato_gif(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="homer.gif")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 404
    assert "Page Not Found" in response.text


# Media
@pytest.mark.xfail(reason="Deberia devolver un 400 o 404 ya que no deberia aceptar un formato de imagen .zip")
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_TC038_Verificar_error_de_un_libro_con_imagen_en_formato_zip(get_url, get_token, setup_delete_books_by_id):
    payload = create_request_shelves_imagen_super_modified(image_name="Bug Advocacy.zip")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(method="POST",
                 url=response.url,
                 headers=response.headers,
                 payload=payload,
                 token=TOKEN,
                 response=response
                 )
    assert response.status_code == 404
    assert "Page Not Found" in response.text