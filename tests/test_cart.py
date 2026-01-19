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

    @pytest.mark.positive
    def test_get_carts_with_limit(self,api_client):
        limit =5
        response=api_client.get("/carts",params={"limit":limit})
        data =response.json()
        assert len(data) == limit

    @pytest.mark.positive
    def test_get_carts_with_sort(self,api_client):
        order ={"desc","asc"}
        for sort_order in order:
            response=api_client.get("/carts",params={"sort":sort_order})
            ResponseValidator.validate_status_code(response,200)
            ResponseValidator.validate_array_not_empty(response)
            data =response.json()
            ids =[cart["id"] for cart in data]
            sorted_ids =sorted(ids,reverse=(sort_order=="desc"))
            assert ids == sorted_ids

    @pytest.mark.positive
    def test_get_cart_in_daterange(self,api_client):
        start_date ="2020-01-01"
        end_date ="2020-12-31"
        response=api_client.get("/carts",params={"startdate":start_date,"enddate":end_date})
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_array_not_empty(response)
        data =response.json()
        for cart in data:
            assert start_date <= cart["date"] <= end_date

    @pytest.mark.positive
    def test_get_carts_with_startdate_only(self,api_client):
        start_date ="2020-06-01"
        response=api_client.get("/carts",params={"startdate":start_date})
        data =response.json()
        for cart in data:
            assert cart["date"] >= start_date

    @pytest.mark.positive
    def test_get_carts_with_enddate_only(self,api_client):
        end_date ="2020-06-30"
        response=api_client.get("/carts",params={"enddate":end_date})
        data =response.json()
        for cart in data:
            assert cart["date"] <= end_date

    @pytest.mark.negative
    def test_get_carts_with_invalid_dateformat(self,api_client):
        invalid_dates =["2020/01/01","01-01-2020","June 1, 2020"]
        for date in invalid_dates:
            response=api_client.get("/carts",params={"startdate":date})
            ResponseValidator.validate_empty_response(response)
            response=api_client.get("/carts",params={"enddate":date})
            ResponseValidator.validate_empty_response(response)

    @pytest.mark.positive
    def test_create_cart(self,api_client):
        new_cart ={
            "userId":3,
            "date":"2023-10-01",
            "products":[
                {"productId":1,"quantity":2},
                {"productId":2,"quantity":1}
            ]
        }
        response=api_client.post("/carts",data=new_cart)
        ResponseValidator.validate_status_code(response,201)
        data =response.json()
        SchemaValidator.Validate_cart_schema(data)
        assert data["userId"] == new_cart["userId"]
        assert data["date"] == new_cart["date"]
        assert data["products"] == new_cart["products"]

    @pytest.mark.negative
    def test_create_cart_with_invalid_data(self,api_client):
        invalid_carts =[
            {
                "userId":"abc",
                "date":"2023-10-01",
                "products":[{"productId":1,"quantity":2}]
            },
            {
                "userId":3,
                "date":"10-01-2023",
                "products":[{"productId":1,"quantity":2}]
            },
            {
                "userId":3,
                "date":"2023-10-01",
                "products":"invalid_products"
            }
        ]
        for cart in invalid_carts:
            response=api_client.post("/carts",data=cart)
            ResponseValidator.validate_empty_response(response)

    