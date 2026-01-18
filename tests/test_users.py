from utils.api_client import APIClient
import pytest
from validators.response_validator import ResponseValidator
from validators.schema_validator import SchemaValidator

@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.mark.users
class TestUsers:

    @pytest.mark.positive
    def test_get_all_users(self,api_client):
        response=api_client.get("/users")
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_array_not_empty(response)
        ResponseValidator.validate_response_time(response,api_client.timeout)
        SchemaValidator.Validate_user_schema(response.json()[0])

    @pytest.mark.positive
    def test_get_user_by_id(self,api_client):
        response=api_client.get("/users/1")
        ResponseValidator.validate_status_code(response,200)
        data =response.json()
        SchemaValidator.Validate_user_schema(data)
        assert data["id"] ==1

    @pytest.mark.negative
    def test_get_user_by_invalid_id(self,api_client):
        ids = ["abc","!@#"]
        for user_id in ids:
            response=api_client.get(f"/users/{user_id}")
            ResponseValidator.validate_invalid_response(response)

    @pytest.mark.positive
    def test_get_users_with_limit(self,api_client):
        limit =5
        response =api_client.get("/users",params ={"limit":limit})
        ResponseValidator.validate_status_code(response,200)
        ResponseValidator.validate_array_not_empty(response)
        data =response.json()
        assert len(data) == limit
        for user in data:
            SchemaValidator.Validate_user_schema(user)
 
    @pytest.mark.positive
    def test_get_users_with_sort(self,api_client):
        order ={"desc","asc"}
        for sort_order in order:
            response =api_client.get("/users",params={"sort":sort_order})
            ResponseValidator.validate_status_code(response,200)
            ResponseValidator.validate_array_not_empty(response)
            data =response.json()
            ids = [user["id"] for user in data]
            sorted_ids = sorted(ids,reverse=(sort_order=="desc"))
            assert ids == sorted_ids

    @pytest.mark.negative
    def test_get_users_with_invalid_limit(self,api_client):
        invalid_limits =["abc"]
        for limit in invalid_limits:
            response=api_client.get("/users",params={"limit":limit})
            ResponseValidator.validate_empty_response(response)

    @pytest.mark.positive
    def test_create_user(self,api_client):
        data_user={
            "id":11,
            "username":"testuser",
            "password":"testpass",
            "email":"testuser@gmail.com"
        }
        response=api_client.post("/users",data=data_user)
        ResponseValidator.validate_status_code(response,201)
        response_data=response.json()
        assert "id" in response_data, "Response must contain user ID"
        user_id = response_data["id"]
        assert user_id > 0, f"User ID must be positive, got {user_id}"

    @pytest.mark.negative
    def test_create_user_missing_fields(self,api_client):
        incomplete_user_data ={
            "username":"incompleteuser"
        }
        response=api_client.post("/users",data=incomplete_user_data)
        ResponseValidator.validate_empty_response(response)

    @pytest.mark.negative
    def test_create_user_invalid_email(self,api_client):
        invalid_emails =["","user@.com"]
        for email in invalid_emails:
            invalid_user_data={
                "username":"invalidemailuser",
                "password":"somepass",
                "email":email
            }
            response=api_client.post("/users",data=invalid_user_data)
            ResponseValidator.validate_empty_response(response)

    