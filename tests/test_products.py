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

    @pytest.mark.negative 
    @pytest.mark.xfail(reason="API allows negative limit and returns all products")
    def test_get_products_with_negative_limit(self,api_client):
        response =api_client.get("/products",params={"limit":-5})
        #This should be 400 but returns 100
        ResponseValidator.validate_status_code(response,400)
        data =response.json()
        #This should be empty but returns 15
        assert len(data)== 0

    @pytest.mark.positive
    def test_get_all_products(self,api_client):
        response = api_client.get("/products/categories")
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        ResponseValidator.validate_array_not_empty(response)
        data =response.json()
        assert len(data) >0

    @pytest.mark.positive
    def test_get_products_by_category(self,api_client):
        categories =["electronics","jewelery","men's clothing","women's clothing"]
        for category in categories:
            response =api_client.get(f"/products/category/{category}")
            ResponseValidator.validate_status_code(response,200)
            ResponseValidator.validate_response_time(response,api_client.timeout)
            ResponseValidator.validate_array_not_empty(response)
            data =response.json()
            for product in data:
                assert product["category"] == category
                assert SchemaValidator.Validate_product_schema(product)

    @pytest.mark.negative
    def test_get_products_by_invalid_category(self,api_client):
        invalid_categories =["","!@#$%"]
        for category in invalid_categories:
            response =api_client.get(f"/products/category/{category}")
            ResponseValidator.validate_product_not_found(response)

    @pytest.mark.positive
    def test_create_new_product(self,api_client):
        new_product ={
            "title": "Test Product",
            "price": 29.99,
            "description": "This is a test product",
            "image": "https://i.pravatar.cc",
            "category": "electronics"
        }
        response =api_client.post("/products",data=new_product)
        ResponseValidator.validate_status_code(response,201)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        data =response.json()
        assert "id" in data is not None
        assert data["title"] == new_product["title"]
        assert data["price"] == new_product["price"]
        assert data["description"] == new_product["description"]
        assert data["category"] == new_product["category"]
        assert SchemaValidator.Validate_product_schema(data)

    @pytest.mark.negative
    @pytest.mark.xfail(reason="API allows creation without title and returns 201")
    def test_create_product_without_title(self,api_client):
        object ={
            "price": 0.1,
            "description": "string",
            "category": "string",
            "image": "http://example.com"
        }
        response =api_client.post("/products",data=object)
        #This should be 400 but API returns 201
        ResponseValidator.validate_status_code(response,400)

    @pytest.mark.negative
    @pytest.mark.xfail(reason="API allows invalid price and returns 201")
    def test_create_product_with_invalid_price(self,api_client):
        invalid_prices =[ -10, "abc", None]
        for price in invalid_prices:
            object ={
                "title": "Invalid Price Product",
                "price": price,
                "description": "This product has invalid price",
                "image": "https://i.pravatar.cc",
                "category": "electronics"
            }
            response =api_client.post("/products",data=object)
            #This should be 400 but API returns 201
            ResponseValidator.validate_status_code(response,400)

    @pytest.mark.positive
    def test_create_product_with_longtitle(self,api_client):
        long_title ="L" * 1000  #1000 characters long
        new_product ={
            "title": long_title,
            "price": 49.99,
            "description": "Product with a very long title",
            "image": "https://i.pravatar.cc",
            "category": "jewelery"
        }
        response =api_client.post("/products",data=new_product)
        ResponseValidator.validate_status_code(response,201)
        data =response.json()
        assert data["title"] == long_title
        assert SchemaValidator.Validate_product_schema(data)

    @pytest.mark.negative
    @pytest.mark.xfail(reason="API allows empty description and returns 201")
    def test_create_product_with_empty_description(self,api_client):
        product ={
            "title": "No Description Product",
            "price": 19.99,
            "description": "",
            "image": "https://i.pravatar.cc",
            "category" : "makeup"
        }
        response =api_client.post("/products",data=product)
        #This should be 400 but API returns 201
        ResponseValidator.validate_status_code(response,400)

    @pytest.mark.positive
    def test_update_product(self,api_client):
        updated_data ={
            "title": "Updated Product Title",
            "price": 39.99,
            "description": "This is an updated description",
            "image": "https://i.pravatar.cc",
            "category" : "skincare"
        }
        response=api_client.put("/products/1",data=updated_data)
        ResponseValidator.validate_status_code(response,200)
        product =response.json()
        assert product["title"] == updated_data["title"]
        assert product["price"] == updated_data["price"]
        assert product["description"] == updated_data["description"]
        assert product["category"] == updated_data["category"]
        assert SchemaValidator.Validate_product_schema(product)

    @pytest.mark.negative
    def test_update_product_with_invalid_id(self,api_client):
        invalid_ids =["!@#", "abc"]
        updated_data ={
            "title": "Updated Product Title",
            "price": 39.99,
            "description": "This is an updated description",
            "image": "https://i.pravatar.cc",
            "category" : "skincare"
        }
        for id in invalid_ids:
            response =api_client.put(f"/products/{id}",data=updated_data)
            print(id)
            ResponseValidator.validate_invalid_response(response)

    @pytest.mark.negative
    def test_update_empty_product(self,api_client):
        response=api_client.put("/products/1",data={})
        ResponseValidator.validate_product_not_found(response)

    @pytest.mark.positive
    def test_update_product_title(self,api_client):
        response=api_client.patch("/products/1",data={"title": "Patched Title"})
        ResponseValidator.validate_status_code(response,200)
    
    @pytest.mark.positive
    def test_update_product_price(self,api_client):
        response=api_client.patch("/products/1",data={"price": 59.99})
        ResponseValidator.validate_status_code(response,200)

    @pytest.mark.positive
    def test_update_product_multiple_fields(self,api_client):
        updated_fields ={
            "title": "Multi-field Patch",
            "price": 79.99
        }
        response=api_client.patch("/products/1",data=updated_fields)
        ResponseValidator.validate_status_code(response,200)

    @pytest.mark.positive
    def test_delete_product(self,api_client):
        response=api_client.delete("/products/1")
        ResponseValidator.validate_status_code(response,200)

    @pytest.mark.negative
    def test_delete_product_with_invalid_id(self,api_client):
        invalid_ids =["!@#", "abc"]
        for id in invalid_ids:
            response=api_client.delete(f"/products/{id}")
            ResponseValidator.validate_invalid_response(response)

    @pytest.mark.negative
    def test_delete_deleted_product(self,api_client):
        api_client.delete("/products/2")  #First delete
        response=api_client.delete("/products/2")  #Try deleting again
        ResponseValidator.validate_product_not_found(response)
