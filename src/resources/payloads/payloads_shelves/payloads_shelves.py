import os
import random
import string
from typing import Union

# Ruta base de tus imágenes
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../data")

def create_request_shelves_imagen_super_modified(
    name: Union[str, None] = None,
    description_html: Union[str, None] = None,
    image_name: Union[str, None] = None
) -> dict:
    payload = {
        "name": _generate_value(name, default_length=10),
        "description_html": _generate_value(description_html, default_length=30)
    }
    # Agregar tags aleatorios
    payload["tags"] = _generate_random_tags()

    # Si el usuario pasó una imagen (por nombre sin extensión)
    if image_name:
        image_path = _find_image_file(image_name)
        if image_path:
            payload["image"] = open(image_path, "rb")
        else:
            print(f" Imagen '{image_name}' no encontrada en carpeta data.")
            payload["image"] = None
    else:
        payload["image"] = None

    return payload


def create_request_shelves_payload(
    name: Union[str, None] = None,
    description: Union[str, None] = None,
    tags: Union[list, None] = None
) -> dict:
    payload = {
        "name": _generate_value(name, default_length=10),
        "description": _generate_value(description, default_length=25),
        "tags": tags if tags is not None else _generate_random_tags()
    }
    return payload

def get_random_title():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

def get_random_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


#sin descripcion
def create_request_shelves_payload_sin_descripcion(
    name: Union[str, None] = None
) -> dict:
    payload = {
        "name": _generate_value(name, default_length=8)
    }
    return payload


#sin name
def create_request_shelves_payload_sin_nombre(
    description: Union[str, None] = None
) -> dict:
    payload = {
        "description": _generate_value(description, default_length=25)
    }
    return payload



def create_request_project_payload_modificado(
    title: str | int | None = None,
    code: str | int | None = None,
    description: str | int | None = None,
) -> dict:

    payload = {
        "title": str(title) if title is not None else get_random_title(),
        "code": str(code) if code is not None else get_random_code(),
        "description": str(description) if description is not None else get_random_code(),
    }
    return payload


import random
import string
from typing import Union

def create_request_shelves_payload_super_modified(
    name: Union[str, None] = None,
    description_html: Union[str, None] = None,
) -> dict:

    payload = {
        "name": _generate_value(name, default_length=10),
        "description_html": _generate_value(description_html,default_length=30)
    }
    return payload

def _generate_value(value, default_length=5):

    if value is None:
        return _random_string(default_length)

    if isinstance(value, int):
        return _random_string(value)

    return str(value)

def _random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def _generate_random_tags():
   """Genera etiquetas aleatorias (opcional para BookStack)."""
   return [
       {"name": "Tipo", "value": random.choice(["QA", "Dev", "Test"])},
       {"name": "Prioridad", "value": random.choice(["Alta", "Media", "Baja"])}
   ]


def _find_image_file(image_name: str) -> Union[str, None]:
    for ext in ["jpeg", "jpg", "png", "gif", "webp"]:
        image_path = os.path.join(DATA_DIR, f"{image_name}.{ext}")
        if os.path.exists(image_path):
            return image_path
    return None