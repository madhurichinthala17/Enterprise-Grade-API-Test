import pytest
import requests
from utils.api_client import APIClient
from validators.schema_validator import SchemaValidator
from validators.response_validator import ResponseValidator


@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()

@pytest.mark.products
class Testproducts:

    @pytest.mark.positive
    def test_get_all_products(self,api_client):
        response = api_client.get("/products")
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        ResponseValidator.validate_array_not_empty(response)
        data =response.json()
        for product in data:
            assert SchemaValidator.Validate_product_schema(product)


   





