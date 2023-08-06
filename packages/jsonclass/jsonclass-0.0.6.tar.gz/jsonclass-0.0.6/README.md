# JSONClass

Convert json to object and back in Python. 

## Example

    from jsonclass import JSONClass
  
  
    class Test(JSONClass):
        field: str
  
  
    obj = Test()
    obj.field = "value"
    assert obj.to_json()["field"] == "value"
  
    obj = JSONClass({"__json_class__": "Test", "field": "value2"})
    assert isinstance(obj, Test)
    assert obj.field = "value2"
