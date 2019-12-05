"""
test_pretty_jsonschema
----------------------------------
Tests for `pretty_jsonschema.json_bases` module.
"""

import pytest
import jsonschema
from pretty_jsonschema.json_bases import (
    JsonBool,
    JsonObject,
    JsonString,
    JsonArray,
    JsonInteger,
    JsonNull,
    JsonNumber
)

NULL = JsonNull()
BOOL = JsonBool()
STRING = JsonString()
INTEGER = JsonInteger()
NUMBER = JsonNumber()
ARRAY = JsonArray()
OBJECT = JsonObject()


# Draft6 tests
test_parameters = (
    # (schema, positive, negative)
    (NULL(), None, "test"),

    (BOOL(), True, "test"),

    (INTEGER(enum=[1, 2, 3]), 2, 22),

    (NUMBER(minimum=1, maximum=5), 2.5, 22.3),
    (NUMBER(exclusiveMinimum=1, exclusiveMaximum=5), 2.5, 5),
    (NUMBER(multipleOf=10), 10, 98),
    (NUMBER(enum=[1, 2.2, 3.3]), 2.2, 3.4),

    (STRING(minLength=1, maxLength=6), "abcdef", "abcdefgh"),
    (STRING(pattern=r"\d{1,3}-\d{1,3}"), "123-123", "123-asd"),
    (STRING(enum=["alubaba", "robber"]), "alubaba", "haha"),

    (ARRAY(items=STRING()), ["test1", "test2"], [1, 2]),
    (ARRAY(items=[STRING(), INTEGER(), NULL()]), ["test1", 123, None], [123, "test1", None]),
    (ARRAY(items=[STRING(), INTEGER()], additionalItems=False), ["test1", 123], [123, "test1", None]),
    (ARRAY(contains=STRING()), ["test1", 123, None], [123, 234, None]),
    (ARRAY(minItems=1, maxItems=3), ["test1", 123, None], [123, ["asd"], None, None]),
    (ARRAY(uniqueItems=True), [1, 2, 3, 4], [1, 2, 2, 3]),

    (OBJECT(properties={"test1": INTEGER()}), {"test1": 1}, {"test1": "testing"}),
    (OBJECT(properties={"test1": INTEGER()},
            additionalProperties=False),
     {"test1": 1}, {"test1": 1, "test2": "testing"}),
    # required all
    (OBJECT(properties={"test1": INTEGER(), "test2": INTEGER()},
            required=True),
     {"test1": 1, "test2": 2}, {"test1": 1}),
    # required some
    (OBJECT(properties={"test1": INTEGER(), "test2": INTEGER()},
            required=["test1"]),
     {"test1": 1}, {"test2": 2}),
    # required any
    (OBJECT(properties={"test1": INTEGER(), "test2": INTEGER(), "test3": INTEGER()},
            anyOf=["test1", "test2"]),
     {"test1": 1, "test3": 3}, {"test3": 3}),
    (OBJECT(minProperties=1,
            maxProperties=3),
     {"test1": 1, "test2": 2}, {"test1": 1, "test2": 2, "test3": 3, "test4": 4}),
    (OBJECT(patternProperties={r"^test\d$": INTEGER()},
            additionalProperties=False),
     {"test1": 1, "test2": 2}, {"test1": 1, "test2": 2, "test33": 3, "test44": 4}),
    (OBJECT(properties={"test1": INTEGER(), "test2": INTEGER(), "test3": INTEGER()},
            dependencies={"test3": ["test2"]},
            required=["test1"]),
     {"test1": 1}, {"test1": 1, "test3": 3}),
)


@pytest.fixture(scope="function", params=test_parameters)
def params_test(request):
    return request.param


def test_schema(params_test):
    schema, positive, negative = params_test
    assert jsonschema.validate(positive, schema) is None
    try:
        jsonschema.validate(negative, schema)
    except jsonschema.exceptions.ValidationError:
        return
    else:
        raise AssertionError("Schema validated. Expected: ValidationError")
