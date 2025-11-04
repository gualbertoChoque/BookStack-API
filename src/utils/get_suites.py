import requests

def assert_get_suites_assertion(get_url, get_token, code):
    url = f"{get_url}{code}"
    headers = get_token
    response = requests.get(url, headers=headers)
    return response