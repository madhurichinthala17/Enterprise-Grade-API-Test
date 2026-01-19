import pytest
from validators.response_validator import ResponseValidator
from validators.schema_validator import SchemaValidator
from utils.api_client import APIClient


@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.mark.carts
class TestCarts:

    @pytest.mark.positive
    def test_get_all_carts(self,api_client):
        response=api_client.get("/carts")
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_array_not_empty(response)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        SchemaValidator.Validate_cart_schema(response.json()[0])
        