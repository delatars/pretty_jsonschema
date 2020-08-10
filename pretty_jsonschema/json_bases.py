from _collections_abc import Mapping
from typing import Dict, List, Union


__author__ = "Alexandr Morokov"
__email__ = 'morocov.ap.muz@gmail.com'
__version__ = '1.0.0'


class _JsonBase(Mapping):
    """ Base class implements abstract Json type.
    You must use call, to return <dict> object to jsonschema.validate to prevent errors.

    '>>> STRING = JsonString(minLength=1)'
    '>>> STRING'
    {'type': 'string', 'minLength': 1}
    '>>> type(STRING)'
    <class 'test.JsonString'>

    '>>> STRING()'
    {'type': 'string', 'minLength': 1}
    '>>> type(STRING())'
    <class 'dict'>
    """

    JSON_TYPE = "base"

    _INIT_PROPERTIES = {}
    _CALL_PROPERTIES = {}

    @property
    def BASE(self):
        return {"type": self.JSON_TYPE}

    def __init__(self):
        self._data = {**self.BASE,
                      **{prop: value for prop, value in self._INIT_PROPERTIES.items() if value is not None}}

    def __call__(self):
        return {**self._data,
                **{prop: value for prop, value in self._CALL_PROPERTIES.items() if value is not None}}

    def __init_subclass__(cls, JSON_TYPE, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.JSON_TYPE = JSON_TYPE

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        keys = list(self._data)
        for key in keys:
            yield key

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        vals = (f"{k}={v}" for k, v in self._data.items())
        return f"{self.__class__.__name__}({', '.join(vals)})"


class JsonNull(_JsonBase, JSON_TYPE="null"):
    """https://json-schema.org/understanding-json-schema/reference/null.html"""


class JsonBool(_JsonBase, JSON_TYPE="boolean"):
    """https://json-schema.org/understanding-json-schema/reference/boolean.html"""


class JsonInteger(_JsonBase, JSON_TYPE="integer"):
    """https://json-schema.org/understanding-json-schema/reference/numeric.html"""

    def __init__(self, enum: List = None):
        self._INIT_PROPERTIES = {"enum": enum}
        super().__init__()

    def __call__(self, enum=None):
        self._CALL_PROPERTIES = {"enum": enum}
        return super().__call__()


class JsonNumber(_JsonBase, JSON_TYPE="number"):
    """https://json-schema.org/understanding-json-schema/reference/numeric.html"""

    def __init__(self,
                 multipleOf: int = None,
                 minimum: int = None,
                 exclusiveMinimum: int = None,
                 maximum: int = None,
                 exclusiveMaximum: int = None,
                 enum: List = None):
        self._INIT_PROPERTIES = {
            "multipleOf": multipleOf,
            "minimum": minimum,
            "exclusiveMinimum": exclusiveMinimum,
            "maximum": maximum,
            "exclusiveMaximum": exclusiveMaximum,
            "enum": enum
        }
        super().__init__()

    def __call__(self,
                 multipleOf: int = None,
                 minimum: int = None,
                 exclusiveMinimum: int = None,
                 maximum: int = None,
                 exclusiveMaximum: int = None,
                 enum: List = None):
        self._CALL_PROPERTIES = {
            "multipleOf": multipleOf,
            "minimum": minimum,
            "exclusiveMinimum": exclusiveMinimum,
            "maximum": maximum,
            "exclusiveMaximum": exclusiveMaximum,
            "enum": enum
        }
        return super().__call__()


class JsonString(_JsonBase, JSON_TYPE="string"):
    """https://json-schema.org/understanding-json-schema/reference/string.html"""

    def __init__(self,
                 minLength: int = None,
                 maxLength: int = None,
                 pattern: str = None,
                 format: str = None,
                 enum: List = None):
        self._INIT_PROPERTIES = {
            "minLength": minLength,
            "maxLength": maxLength,
            "pattern": pattern,
            "format": format,
            "enum": enum
        }
        super().__init__()

    def __call__(self,
                 minLength: int = None,
                 maxLength: int = None,
                 pattern: str = None,
                 format: str = None,
                 enum: List = None):
        self._CALL_PROPERTIES = {
            "minLength": minLength,
            "maxLength": maxLength,
            "pattern": pattern,
            "format": format,
            "enum": enum
        }
        return super().__call__()


class JsonArray(_JsonBase, JSON_TYPE="array"):
    """https://json-schema.org/understanding-json-schema/reference/array.html"""

    def __init__(self, items: Union[_JsonBase, List[_JsonBase]] = None,
                 contains: Union[_JsonBase, List[_JsonBase]] = None,
                 minItems: int = None,
                 maxItems: int = None,
                 additionalItems: bool = None,
                 uniqueItems: bool = None):
        self._INIT_PROPERTIES = {
            "items": items,
            "contains": contains,
            "minItems": minItems,
            "maxItems": maxItems,
            "additionalItems": additionalItems,
            "uniqueItems": uniqueItems
        }
        super().__init__()

    def __call__(self, items: Union[_JsonBase, List[_JsonBase]] = None,
                 contains: Union[_JsonBase, List[_JsonBase]] = None,
                 minItems: int = None,
                 maxItems: int = None,
                 additionalItems: bool = None,
                 uniqueItems: bool = None):
        self._CALL_PROPERTIES = {
            "items": items,
            "contains": contains,
            "minItems": minItems,
            "maxItems": maxItems,
            "additionalItems": additionalItems,
            "uniqueItems": uniqueItems
        }
        return super().__call__()


class JsonObject(_JsonBase, JSON_TYPE="object"):
    """https://json-schema.org/understanding-json-schema/reference/object.html"""

    def __init__(self, properties: Dict[str, Union[_JsonBase, List[_JsonBase]]] = None,
                 patternProperties: Dict[str, Union[_JsonBase, List[_JsonBase]]] =None,
                 additionalProperties: Union[bool, _JsonBase] = None,
                 required: Union[bool, List[str]] = None,
                 anyOf: List[str] = None,
                 propertyNames: Dict[str, str] = None,
                 minProperties: int = None,
                 maxProperties: int = None,
                 dependencies: Dict[str, List[str]] = None):

        self._check_for_multiple_types(properties)

        self._INIT_PROPERTIES = {
            "properties": properties,
            "patternProperties": patternProperties,
            "additionalProperties": additionalProperties,
            "required": required,
            "propertyNames": propertyNames,
            "minProperties": minProperties,
            "maxProperties": maxProperties,
            "dependencies": dependencies,
        }

        self._check_required(required, properties)
        self._check_anyOf(anyOf)
        super().__init__()

    def __call__(self, properties: Dict[str, Union[_JsonBase, List[_JsonBase]]] = None,
                 patternProperties: Dict[str, Union[_JsonBase, List[_JsonBase]]] =None,
                 additionalProperties: Union[bool, _JsonBase] = None,
                 required: Union[bool, List[str]] = None,
                 anyOf: List[str] = None,
                 propertyNames: Dict[str, str] = None,
                 minProperties: int = None,
                 maxProperties: int = None,
                 dependencies: Dict[str, List[str]] = None):

        self._check_for_multiple_types(properties)

        self._CALL_PROPERTIES = {
            "properties": properties,
            "patternProperties": patternProperties,
            "additionalProperties": additionalProperties,
            "required": required,
            "propertyNames": propertyNames,
            "minProperties": minProperties,
            "maxProperties": maxProperties,
            "dependencies": dependencies,
        }

        self._check_required(required, properties)
        self._check_anyOf(anyOf)
        return super().__call__()

    def _check_for_multiple_types(self, properties):
        if properties is not None:
            for prop, prop_value in properties.items():
                if isinstance(prop_value, (tuple, list)):
                    new_values = {"type": []}
                    for value in prop_value:
                        try:
                            new_values["type"] += [value.pop("type")]
                            new_values.update(value)
                            properties[prop] = new_values
                        except KeyError:
                            pass

    def _check_required(self, required, properties):
        if isinstance(required, bool):
            if required:
                self._CALL_PROPERTIES["required"] = [field for field in properties.keys()]
            else:
                del self._CALL_PROPERTIES["required"]

    def _check_anyOf(self, anyOf):
        if anyOf:
            self._CALL_PROPERTIES["anyOf"] = [{"required": [field]} for field in anyOf]
