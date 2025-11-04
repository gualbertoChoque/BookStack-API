import jsonschema
import pytest

from src.utils.load_resources import load_schema_resource_by_directory_for_compare


def assert_response_schema(response, json_file, directory):
    schema = load_schema_resource_by_directory_for_compare(json_file, directory)
    try:
        jsonschema.validate(instance=response, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        pytest.fail(f"JSON schema dont match: {err}")

def assert_response_status_code_global(expected_code, status_code):
        assert status_code == expected_code, f"Status esperado {expected_code}, Status obtenido {status_code}"