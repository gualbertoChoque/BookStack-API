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
def test_TC001_Actualizar_un_libro_existente_con_datos_validos(get_url, get_token, setup_add_books,
                                                               setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]

    payload = create_request_shelves_payload_super_modified(name="Libro_Actualizado",
                                                            description_html="Descripción actualizada desde test automatizado"
                                                            )
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    assert "Descripción actualizada" in response.json()[
        "description_html"], "La descripción no se actualizó correctamente"
    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC002_Verificar_que_de_error_al_enviar_una_URL_mal_formada_al_actualiza_un_libro(get_invalid_url, get_token,
                                                                                    setup_add_books,
                                                                                    setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.put.value, get_invalid_url, StaticDataModules.books.value,
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

    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC003_Actualizar_un_libro_con_el_mismo_nombre(get_url, get_token, setup_add_books,
                                                             setup_delete_books_by_id):
    shelf_creado = setup_add_books
    id_to_update = shelf_creado["id"]

    payload = create_request_shelves_payload_super_modified(name=shelf_creado["name"])

    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.negative
@pytest.mark.regression
def test_TC004_Verificar_que_permita_actualizar_un_libro_con_un_body_basio(get_url, get_token, setup_add_books,
                                                                               setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = {}
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.no_content_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )
    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.negative
@pytest.mark.regression
def test_TC005_Verificar_que_no_permita_crear_un_libro_con_un_token_incorrecto(get_url, get_token):
    payload = create_request_shelves_payload_super_modified()
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.post.value, get_url, StaticDataModules.books.value, None,
                                StaticDataHeaders.invalid_token_header.value, json.dumps(payload))

    log_api_call(method="PUT",
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
def test_TC006_Verificar_que_no_permita_actualizar_un_libro_con_un_token_incorrecto(get_url, get_token,
                                                                                        setup_add_books,
                                                                                        setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]

    payload = create_request_shelves_payload_super_modified()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC007_Verificar_que_no_permita_crear_un_libro_sin_autentificar(get_url, get_token, setup_add_books,
                                                                            setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]

    payload = create_request_shelves_payload_super_modified()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC008_Verificar_actualizar_libros_sin_description(get_url, get_token, setup_add_books,
                                                              setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion()
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)

    assert response.json()["id"] == id_to_update
    assert response.json()["name"] == payload["name"]
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC009_Actualizar_un_libro_con_nombre_nuevo_en_mayusculas(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="LIBRO")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC010_Actualizar_un_libro_con_nombre_nuevo_en_minusculas(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="pruebas")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC011_Actualizar_un_libros_con_nombre_nuevo_numerico(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="12345")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC012_Actualizar_un_libro_con_nombre_nuevo_con_caracteres_especiales(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="%$#@&$")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC013_Actualizar_un_libro_con_nombre_con_espacio_en_medio(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion("Act ualizado")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC014_Actualizar_un_libro_con_nombre_con_espacio_al_inicio(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion("   Actualizado")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC015_Actualizar_un_libro_con_nombre_con_espacio_al_final(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion("Actualizado2    ")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un libro con nombre de espacios")
@pytest.mark.negative
@pytest.mark.regression
def test_TC016_Verificar_que_no_permita_actualizar_un_libro_con_solo_espacios(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(name="    ")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC017_Actualizar_un_libro_con_nombre_alfa_numerico_mixto(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name="Shelf123Mix")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Alta
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un libro sin nombre")
@pytest.mark.negative
@pytest.mark.regression
def test_TC018_Verificar_que_no_permita_actualizar_un_libro_con_nombre_nulo(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(name="")
    assert_response_schema(payload, "add_books_schema_request.json", "schemas_books")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC019_Verificar_actualizar_de_un_libro_con_nombre_de_1_solo_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=1)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.regression
@pytest.mark.positive
def test_TC020_Verificar_actualizar_de_un_libro_con_nombre_de_2_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=2)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC021_Verificar_actualizar_de_un_libro_con_nombre_de_254_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=254)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC022_Verificar_actualizar_de_un_libro_con_nombre_de_255_solo_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=225)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC023_Verificar_actualizar_de_un_libro_con_nombre_de_125_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=125)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC024_Verificar_actualizar_de_un_libros_con_nombre_de_256_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=256)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC025_Verificar_actualizar_de_un_libros_con_nombre_de_280_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_sin_descripcion(name=280)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC026_Verificar_la_actualizacion_de_un_libro_con_imagen(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_imagen_super_modified(image_name="alimentos.jpeg")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.xfail(reason="Deberia devolver un 422 ya que no esta permitido tener un libro sin nombre y sin descripcion")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC027_Verificar_que_no_permita_actualizar_un_libros_con_con_todos_los_campos_vacíos(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(name="", description_html="")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
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
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC028_Verificar_actualizar_de_un_libros_con_descripcion_de_1_solo_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(description_html=1)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC029_Verificar_actualizar_de_un_libro_con_descripcion_de_256_carácter(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(description_html=256)
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC030_Verificar_actualizar_de_un_libro_con_espacios_en_descripcion(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(description_html="         ")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)


# Media
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.positive
def test_TC031_Verificar_actualizar_de_un_libro_con_descripcion_basio(get_url, get_token, setup_add_books,
                                                                      setup_delete_books_by_id):
    id_to_update = setup_add_books["id"]
    payload = create_request_shelves_payload_super_modified(description_html="")
    response = request_function(StaticDataVerbs.put.value, get_url, StaticDataModules.books.value,
                                f"{id_to_update}", StaticDataHeaders.default_header.value, json.dumps(payload))

    log_api_call(
        method="PUT",
        url=response.url,
        headers=response.headers,
        payload=payload,
        token=get_token,
        response=response
    )

    assert_response_schema(response.json(), "add_books_schema_response.json", "schemas_books")
    assert_response_status_code_global(200, response.status_code)
    assert response.json()["id"] == id_to_update
    setup_delete_books_by_id(id_to_update)