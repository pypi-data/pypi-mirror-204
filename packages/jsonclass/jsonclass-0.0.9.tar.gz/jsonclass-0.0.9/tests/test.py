import jsonclass
from jsonclass import JSONClass


class Test(JSONClass):
    field: str


test = Test()
test.field = "test"
serialized = jsonclass.dumps(test)
deserialized = jsonclass.loads(serialized)
assert isinstance(deserialized, Test)
assert deserialized.field == "test"
