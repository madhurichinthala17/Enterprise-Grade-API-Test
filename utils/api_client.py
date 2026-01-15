import pytest
from config.config import Config
import requests

class APIClient:
    def __init__(self):
        self.base_url= Config.BASEURL
        self.timeout = Config.TIMEOUT
        self.headers=Config.HEADERS.copy()
        self.session=requests.sessions.Session()

    def get(self,endpoint,headers=None,params=None):
        url = f"{self.base_url}{endpoint}"
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        try:
            response =self.session.get(url,
                                       headers=request_headers,
                                       timeout=self.timeout,
                                       params=params)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            raise

    def post(self,endpoint,data=None,headers=None):
        url=f"{self.base_url}{endpoint}"
        request_headers=self.headers.copy()
        if headers:
            request_headers=self.headers.update(headers)

        try:
            response=self.session.post(url,
                                       json=data,
                                       headers=request_headers,
                                       timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            raise

    def delete(self,endpoint,headers=None):
        url=f"{self.base_url}{endpoint}"
        request_headers=self.headers.copy()
        if headers:
            request_headers.update(headers)
        try:
            response=self.session.delete(url,
                                         headers=request_headers,
                                         timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            raise

    def close(self):
        """Close the requests session"""
        self.session.close()

