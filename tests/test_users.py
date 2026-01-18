from utils.api_client import APIClient
import pytest
from validators.response_validator import ResponseValidator
from validators.schema_validator import SchemaValidator

@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()

@pytest.mark.postive
@pytest
def test_get_all_users(self,api_client):
    response=api_client.get("/users")
    ResponseValidator.validate_status_code(response,200)
    ResponseValidator.validate_array_not_empty(response)
    ResponseValidator.validate_response_time(response,api_client.timeout)
