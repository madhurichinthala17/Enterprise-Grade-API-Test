import time

class ResponseValidator:
    #validate status code
    def validate_status_code(response,expected_statuscode):
        assert response.status_code == expected_statuscode
        return True
    def validate_response_time(response,max_response_time):
        response_time = response.elapsed.total_seconds()
        assert response_time <= max_response_time
        return True
    def validate_array_not_empty(response):
        try:
            data =response.json()
            assert isinstance(data,list) and len(data) >0
            return True
        except ValueError:
            raise AssertionError("Response is not a valid JSON array")