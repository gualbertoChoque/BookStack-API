import random
import string

def create_request_project_payload(
    title: str | int | None = None,
    code: str | int | None = None,
    description: str | int | None = None,
) -> dict:
    payload = {
        "title": get_random_title() if title is None else str(title),
        "code": get_random_code() if code is None else str(code),
        "description": get_random_code() if description is None else str(description),
    }
    return payload

def get_random_title():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

def get_random_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


#sin descripcion
def create_request_project_payload_Sin_descripcion(
    title: str | int | None = None,
    code: str | int | None = None,
) -> dict:
    payload = {
        "title": get_random_title() if title is None else str(title),
        "code": get_random_code() if code is None else str(code),
    }
    return payload



#sin title
def create_request_project_payload_Sin_title(
        code: str | int | None = None,
        description: str | int | None = None,
) -> dict:
    payload = {
        "code": get_random_code() if code is None else str(code),
        "description": get_random_code() if description is None else str(description),
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


