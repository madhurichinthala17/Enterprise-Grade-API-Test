import jsonschema
from jsonschema import validators
import time

class ResponseValidator:
    
    #validating product schema
    def Validate_product_schema(data):
        schema ={
            "type": "object",
            "required": ["id", "title", "price", "description","category", "image"],
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "price": {"type": "number"},
                "description": {"type": "string"},
                "category": {"type": "string"},
                "image": {"type": "string"}
            }   
        }
        try:
            jsonschema.validate(instance=data,schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            raise AssertionError(f"Schema validation error: {e.message}")
    

