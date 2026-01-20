import pytest
from utils.api_client import APIClient
from validators.response_validator import ResponseValidator
from validators.schema_validator import SchemaValidator

@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()

@pytest.mark.integration
class TestIntegration:

    @pytest.mark.positive
    def test_user_cart_integration(self,api_client):

        # Create a new user
        user_data = {
            "email": "username@gmail.com",
            "username": "username",
            "password": "password123"
        }
        user_response =api_client.post("/users",data=user_data)
        ResponseValidator.validate_status_code(user_response,201)
        user =user_response.json()
        user_id =user["id"]

        # Create a new cart for the user
        cart_data ={
            "userId": user_id,
            "date": "2023-10-10",
            "products": [
                {"productId": 1, "quantity": 2},
                {"productId": 2, "quantity": 1}
            ]
        }
        cart_response =api_client.post("/carts",data=cart_data)
        ResponseValidator.validate_status_code(cart_response,201)
        cart =cart_response.json()
        assert cart["userId"] == user_id

    @pytest.mark.positive
    def test_product_cart_integration(self,api_client):

        #Fetch a product
        response =api_client.get("/products/1")
        ResponseValidator.validate_status_code(response,200)
        product =response.json()
        product_id =product["id"]


        #Create a cart with the product
        cart_data ={
            "userId": 1,
            "date": "2023-10-10",
            "products": [
                {"productId": product_id, "quantity": 3}
            ]
        }
        cart_response =api_client.post("/carts",data=cart_data)
        ResponseValidator.validate_status_code(cart_response,201)
        cart =cart_response.json()
        products_in_cart =cart["products"]
        for product in products_in_cart:
            assert product["productId"] == product_id


