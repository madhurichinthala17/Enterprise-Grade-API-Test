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
        

    @pytest.mark.positive
    def test_get_cart_by_id(self,api_client):
        response =api_client.get("/carts/1")
        ResponseValidator.validate_status_code(response,200)
        data =response.json()
        SchemaValidator.Validate_cart_schema(data)
        assert data["id"] ==1

    @pytest.mark.positive
    def test_get_carts_for_user(self,api_client):
        user_id =1
        response=api_client.get(f"/carts/user/{user_id}")
        ResponseValidator.validate_status_code(response,200)
        data =response.json()
        for cart in data:
            SchemaValidator.Validate_cart_schema(cart)
            assert cart["userId"] == user_id

    @pytest.mark.negative
    def test_get_cart_by_invalid_id(self,api_client):
        ids =["abc","!@#"]
        for cart_id in ids:
            response=api_client.get(f"/carts/{cart_id}")
            ResponseValidator.validate_invalid_response(response)

    @pytest.mark.negative
    def test_get_carts_for_invalid_user(self,api_client):
        ids =["xyz","$%^"]
        for user_id in ids:
            response=api_client.get(f"/carts/user/{user_id}")
            ResponseValidator.validate_invalid_response(response)