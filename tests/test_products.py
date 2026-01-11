import requests

def test_get_all_products():
    response = requests.get('https://fakestoreapi.com/products')
    print(response.json)