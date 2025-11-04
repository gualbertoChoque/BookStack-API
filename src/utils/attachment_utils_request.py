import requests
from config import BASE_URI
import requests

from config import BASE_URI


def delete_request(url: str, headers=None, token_override=None):
    #Envía una petición DELETE
    headers = headers or {}
    response = requests.delete(url, headers=headers)
    return response

def get_request(url: str, headers=None, token_override=None):
    #Envía una petición GET y registra el log de la llamada.
    headers = headers or {}
    response = requests.get(url, headers=headers)
    return response

def build_attachment_url(hash_value: str) -> str:
   # Construye la URL
    hash_value = hash_value.strip() if hash_value else ""
    if hash_value:
        return f"{BASE_URI}/attachment/{hash_value}"
    return f"{BASE_URI}/attachment/"

def build_invalid_url() -> str:
    #Devuelve una URL mal formada
    return f"{BASE_URI}/attac#hment//hash//"
