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

INT32 = 2**31

# When init, we can set default properties.
# Subsequently we can override it by using __call__ method.
STRING = JsonString(minLength=1, maxLength=255, pattern=r"^.*(?!\n)$")
INTEGER = JsonInteger()
NUMBER = JsonNumber(minimum=-INT32, exclusiveMaximum=INT32)
BOOL = JsonBool()
NULL = JsonNull()
ARRAY = JsonArray()
OBJECT = JsonObject()


# Regex patterns
class Patterns:

    ipv4 = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?$)"
    ipv4_with_cidr = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" \
                     r"(?:/3[0-2]|/[1-2]?[0-9])?$"
    hostname = r"^[A-Za-z0-9][A-Za-z0-9\.\-]*$"
    login = r"^[A-Za-z0-9\.\-]*$"
    password = r"^[^\s]*(?!\n)$"
    ldap_uri = r"^ldap[s]?://[A-Za-z0-9\.\-]+$"
    ldap_query = r"^\(.*\)$"


if __name__ == "__main__":
    # Create schema
    LOGIN_SCHEMA = OBJECT(properties={"login": STRING(pattern=Patterns.login),
                                      "password": STRING(pattern=Patterns.password),
                                      "rememberMe": BOOL()},
                          additionalProperties=False,
                          required=True)

    # Check schema
    login_right_data = {"login": "test", "password": "test", "rememberMe": True}
    login_wrong_data = {"login": "", "password": "test", "rememberMe": True}

    print("Check right data.")
    jsonschema.validate(login_right_data, LOGIN_SCHEMA)
    print("Check wrong data.")
    jsonschema.validate(login_wrong_data, LOGIN_SCHEMA)
