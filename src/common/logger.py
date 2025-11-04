
import logging
import allure
from datetime import datetime
from urllib.parse import urlparse
import requests

def setup_logger():
    logger = logging.getLogger("api_logger")
    # Establece el nivel mínimo que registra (DEBUG incluye todo)
    logger.setLevel(logging.DEBUG)
    # Si ya existe algún handler, no volvemos a añadir otro
    if not logger.handlers:
        # Handler que escribe en el archivo "api.log" (modo append)
        handler = logging.FileHandler("api.log", mode="a")
        handler.setLevel(logging.DEBUG)

        # Formato de log: fecha hora, nivel y mensaje
        fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        handler.setFormatter(fmt) # Asigna el formato al handler
        logger.addHandler(handler) # Añade el handler al logger
    return logger

# Creamos un logger
logger = setup_logger()

def log_api_call(
    method:   str,
    url:      str,
    headers:  dict,
    payload:  dict | None,
    token:    str | None,
    response: requests.Response
):
    """
    Agrupa TODO el logging en pasos de Allure:
      • INFO IP/domain
      • DEBUG Authentication
      • DEBUG Request URL + Headers
      • DEBUG Payloads
      • INFO Timestamp (momento de la petición)
      • INFO Status code
      • DEBUG Response headers
      • DEBUG Response payload
    """
    # INFO: HTTP method
    with allure.step("INFO: HTTP method"):
        logger.info(f"HTTP method: {method}")
        allure.attach(method or "", name="HTTP Method", attachment_type=allure.attachment_type.TEXT)
    # Extraemos URL
    domain = urlparse(url).netloc
    # Fecha y hora actual del sistema
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #INFO: IP address or domain
    with allure.step("INFO: IP address or domain"):
        logger.info(f"IP address or domain: {domain}")
        allure.attach(domain, name="Domain", attachment_type=allure.attachment_type.TEXT)
    #DEBUG: Authentication
    with allure.step("DEBUG: Authentication"):
        logger.debug(f"Token: {token}")
        allure.attach(token or "", name="Token", attachment_type=allure.attachment_type.TEXT)
    #DEBUG: Request URL + Headers
    with allure.step("DEBUG: Request URL + Headers"):
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request headers: {headers}")
        allure.attach(url, name="Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(headers), name="Headers", attachment_type=allure.attachment_type.JSON)
    #DEBUG: Payloads
    with allure.step("DEBUG: Payloads"):
        logger.debug(f"Request payload: {payload}")
        allure.attach(str(payload or {}), name="Payload", attachment_type=allure.attachment_type.JSON)
    #INFO: Timestamp of the request
    with allure.step("INFO: Timestamp of the request"):
        logger.info(f"Timestamp: {ts}")
        allure.attach(ts, name="Timestamp", attachment_type=allure.attachment_type.TEXT)
    #INFO: Status code
    with allure.step("INFO: Status code"):
        code = response.status_code
        logger.info(f"Status code: {code}")
        allure.attach(str(code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    #DEBUG: Response headers
    with allure.step("DEBUG: Response headers"):
        hdrs = dict(response.headers)
        logger.debug(f"Response headers: {hdrs}")
        allure.attach(str(hdrs), name="Response Headers", attachment_type=allure.attachment_type.JSON)
    #DEBUG: Response payload
    with allure.step("DEBUG: Response payload"):
        try:
            body = response.json() # Intenta parsear JSON
            logger.debug(f"Response payload: {body}")
            allure.attach(str(body), name="Response Payload", attachment_type=allure.attachment_type.JSON)
        except ValueError:
            # Si no es JSON, adjunta el texto crudo
            text = response.text
            logger.debug(f"Response text: {text}")
            allure.attach(text, name="Response Text", attachment_type=allure.attachment_type.TEXT)
