import jsonschema
import pytest
import requests

from src.utils.load_resources import load_schema_resource


def assert_get_project_assertion(url,token, limit, offset):
        url = f"{url}/project?limit={limit}&offset={offset}"
        headers = {
            'Token': token,
            'accept': 'application/json'
        }

        response = requests.get(url, headers=headers)
        return response

def assert_get_project_response_schema(response, json_file):
    schema = load_schema_resource(json_file)
    try:
        jsonschema.validate(instance=response, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        pytest.fail(f"JSON schema dont match: {err}")
