import jsonclass
from jsonclass import JSONClass


class Test(JSONClass):
    field: str


test = jsonclass.load({"__json_class__": "Test", "field": "value"})
assert isinstance(test, Test)
assert test.field == "value"

test2 = Test()
test2.field = "value"
assert test2.to_json()["field"] == "value"


class Test3(JSONClass):
    child: Test
    l: list
    d: dict
    s: set


test3 = Test3()
assert isinstance(test3.child, Test)
assert isinstance(test3.l, list)
assert isinstance(test3.d, dict)
assert isinstance(test3.s, set)


test4 = jsonclass.load({"__json_class__": "Test3", "child": {"__json_class__": "Test"}})
assert isinstance(test4.child, Test)
