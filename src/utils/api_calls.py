from importlib.metadata import files

import requests
from src.common.url import get_url_parametrized
from src.headers.headers import generate_headers


"""
Funcion para realizar una solicitud
"""

def request_function(method, base_url, module, code=None, header_type=None, payload=None, files_data=None):
    url = get_url_parametrized(base_url, module, code)
    print(url)

    # Si el header es string, generarlo correctamente
    if isinstance(header_type, str):
        from src.headers.headers import generate_headers
        headers = generate_headers(header_type)
    else:
        headers = header_type or {"Accept": "application/json"}

    if isinstance(payload, dict):
        response = requests.request(method, url, headers=headers, json=payload, files=files_data)
    else:
        response = requests.request(method, url, headers=headers, data=payload, files=files_data)

    print(f"[DEBUG] Status code: {response.status_code}")
    return response





#para subir imagenes posible a ser eliminado
def request_function1(method ,get_url, module, code = None, header_type = None, payload = None,files=None):
    url = get_url_parametrized(get_url, module, code)
    print(url)
    headers = generate_headers(header_type)
    response = requests.request(method, url, headers=headers, data=payload,files=files)
    return response