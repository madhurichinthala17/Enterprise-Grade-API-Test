from utils.api_client import APIClient
import pytest


@pytest.fixture(scope="class")
def api_client():
    client = APIClient()
    yield client
    client.close()

@pytest.mark.authentication
class TestAuthentication:

    @pytest.mark.positive
    def test_login_valid_credentials(self,api_client):
        credentials = {
            "username": "mor_2314",
            "password": "83r5^_"
        }
        response = api_client.post("/auth/login", data=credentials)
        assert response.status_code == 201
   

    @pytest.mark.negative
    def test_login_invalid_credentials(self,api_client):
        credentials = {
            "username": "invalidUser",
            "password": "invalidPass"
        }
        response = api_client.post("/auth/login", data=credentials)
        assert response.status_code == 401
  
