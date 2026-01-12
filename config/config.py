"""
Config File for API Testing
"""
import os

class Config:
    BASEURL : os.getenv("BASE_URL","https://fakestoreapi.com") # pyright: ignore[reportInvalidTypeForm]
    TIMEOUT : int(os.getenv("TIMEOUT","10")) # type: ignore

    HEADERS ={
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    }