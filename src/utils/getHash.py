import requests
import io
from src.headers.headers import get_header_with_token1
from config import BASE_URI, TOKEN
from src.common.logger import log_api_call
def obtener_hash_archivo(file_name="archivo_prueba.txt", file_content="Contenido de prueba"):
    url = f"{BASE_URI}/attachment/DEMO"
    # Preparar el archivo en memoria
    file_like = io.BytesIO(file_content.encode('utf-8'))
    files = [('file', (file_name, file_like, 'text/plain'))]
    # Enviar la solicitud
    response = requests.post(url, headers=get_header_with_token1(), files=files)
    # Validar respuesta
    response.raise_for_status()  # Lanza error si no es 200
    data = response.json()
    # Extraer hash
    try:
        hash_value = data["result"][0]["hash"]
    except (KeyError, IndexError):
        raise ValueError("No se encontró el hash en la respuesta.")

    return hash_value
