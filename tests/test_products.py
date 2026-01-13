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

class Testproducts:

    def test_get_all_products(self,api_client):
        response = api_client.get("/products")
        ResponseValidator.validate_status_code(response,200)
        

   





