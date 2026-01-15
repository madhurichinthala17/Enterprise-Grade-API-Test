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

    @pytest.mark.positive
    def test_get_single_product(self,api_client):
        response =api_client.get("/products/1")
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        data =response.json()
        assert data["id"] ==1
        assert SchemaValidator.Validate_product_schema(data)

    @pytest.mark.negative
    def test_get_product_with_invalid_id(self,api_client):
        ids = [99999, -1, "abc",999999999,"!@#"]
        for id in ids:
            response =api_client.get(f"/products/{id}")
            ResponseValidator.validate_product_not_found(response)


    @pytest.mark.positive
    def test_get_limited_products(self,api_client):
        limits =[1,5,20]
        for limit in limits:
            response =api_client.get("/products",params ={"limit":limit})
            ResponseValidator.validate_status_code(response,200)
            length =len(response.json())
            assert length == limit

    @pytest.mark.positive
    def test_get_products_inorder(self,api_client):
        orders =["asc","desc"]
        for order in orders:
            response =api_client.get("/products",params={"sort":order})
            ResponseValidator.validate_status_code(response,200)
            data =response.json()
            prices =[product["id"] for product in data]
            sorted_prices =sorted(prices,reverse=(order=="desc"))
            assert prices == sorted_prices


