from jsonclass import JSONClass


class Test(JSONClass):
    field: str


test = JSONClass({"__json_class__": "Test", "field": "value"})
assert isinstance(test, Test)
assert test.field == "value"

test2 = Test()
test2.field = "value"
assert test2.field == "value"
