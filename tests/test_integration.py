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


    @pytest.mark.positive
    def test_purchase_flow_integration(self,api_client):

        #Login user
        credentials = {
            "username": "mor_2314",
            "password": "83r5^_"
        }
        login_response =api_client.post("/auth/login",data=credentials)
        ResponseValidator.validate_status_code(login_response,201)
        token =login_response.json().get("token")
        api_client.set_auth_token(token)

        #Fetch products
        products_response =api_client.get("/products")
        ResponseValidator.validate_status_code(products_response,200)
        products =products_response.json()  
        assert len(products) >0
        first_product =products[0]
        product_id =first_product["id"]

        #Create cart with a product
        cart_data ={
            "userId": 8,
            "date": "2023-10-10", 
            "products": [
                {"productId": product_id, "quantity": 1}
            ]
        }
        cart_response =api_client.post("/carts",data=cart_data)
        ResponseValidator.validate_status_code(cart_response,201)
        cart =cart_response.json()
        assert cart["userId"] == 8
        assert cart["products"][0]["productId"] == product_id
        

    @pytest.mark.positive
    def test_add_multiple_products_to_cart(self,api_client):
        
        #Create a new cart
        cart_data ={
            "userId": 5,
            "date": "2023-10-15",
            "products": []
        }
        cart_response =api_client.post("/carts",data=cart_data)
        ResponseValidator.validate_status_code(cart_response,201)
        cart =cart_response.json()
        cart_id =cart["id"]

        #Add multiple products to the cart
        products_to_add = [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 3},
            {"productId": 3, "quantity": 1}
        ]
        for product in products_to_add:
            cart["products"].append(product)
        
        update_response =api_client.put(f"/carts/{cart_id}",data=cart)
        ResponseValidator.validate_status_code(update_response,200)
        updated_cart =update_response.json()
        assert len(updated_cart["products"]) == len(products_to_add)

    
    @pytest.mark.positive
    def test_cart_user_validation(self,api_client):
       
       #Create cart for a user
        cart_data ={
            "userId": 6,
            "date": "2023-10-20",
            "products": [
                {"productId": 4, "quantity": 2}
            ]
        }
        cart_response=api_client.post("/carts",data=cart_data)
        ResponseValidator.validate_status_code(cart_response,201)
        cart =cart_response.json()
        user_id =cart["userId"]

        #Fetch user details
        user_response=api_client.get(f"/users/{user_id}")
        ResponseValidator.validate_status_code(user_response,200)
        user =user_response.json()
        assert user["id"] == user_id


    @pytest.mark.positive
    def test_product_availability_in_cart(self,api_client):
         
         #Fetch a product
          product_response =api_client.get("/products/5")
          ResponseValidator.validate_status_code(product_response,200)
          product =product_response.json()
          product_id =product["id"]
    
          #Create a cart with the product
          cart_data ={
                "userId": 7,
                "date": "2023-10-25",
                "products": [
                 {"productId": product_id, "quantity": 1}
                ]
          }
          cart_response=api_client.post("/carts",data=cart_data)
          ResponseValidator.validate_status_code(cart_response,201)
          cart =cart_response.json()
          products_in_cart =cart["products"]
          product_ids_in_cart =[p["productId"] for p in products_in_cart]
          assert product_id in product_ids_in_cart



