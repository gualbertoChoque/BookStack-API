from config import TOKEN, TOKEN_Invalido

def generate_headers(header_type):
    match header_type:
        case "default_header":
            return get_header_with_token()
        case "no_content_header":
            return get_header_without_content()
        case "no_token_header":
            return get_header_without_token()
        case "no_accept_header":
            return get_header_without_accept()
        case "invalid_token_header":
            return get_header_with_invalid_token()
        case _:
            return get_header_with_token()


def get_header_with_token():
    headers = {
        "Accept": "application/json",
        "Authorization": f"{TOKEN}",
        "Content-Type": "application/json"
    }
    return headers


def get_header_without_token():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    return headers


def get_header_without_accept():
    headers = {
        "Authorization": f"{TOKEN}",
        "Content-Type": "application/json"
    }
    return headers


def get_header_without_content():
    headers = {
        "Accept": "application/json",
        "Authorization": f"{TOKEN}"
    }
    return headers


def get_header_with_invalid_token():
    headers = {
        "Accept": "application/json",
        "Authorization": f"{TOKEN_Invalido}",
        "Content-Type": "application/json"
    }
    return headers
