import time

class ResponseValidator:
    #validate status code
    def validate_status_code(response,expected_statuscode):
        assert response.status_code == expected_statuscode
        return True