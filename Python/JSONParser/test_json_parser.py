from json_parser import JsonGenerator
import json
import pytest


# test json parser
def test_primitive_types_json():
    test_str = (
        '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null}'
    )
    json_parser = JsonGenerator()
    assert json_parser.parse(test_str) == json.loads(test_str)


def test_nested_json():
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}}'
    json_parser = JsonGenerator()
    assert json_parser.parse(test_str) == json.loads(test_str)


def test_array_json():
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3]}'
    json_parser = JsonGenerator()
    assert json_parser.parse(test_str) == json.loads(test_str)


def test_unvalid_json():
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3}'
    json_parser = JsonGenerator()
    with pytest.raises(JsonGenerator.JsonSyntaxError):
        json_parser.parse(test_str)


def test_multinested_json():
    test_str = '{"object" : {"type": {"number": 1, "string": "hello", "array": [1,2,3], "object": {"a": "b"}}}}'
    json_parser = JsonGenerator()

    def test_invalid_json():
        test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3}'
        json_parser = JsonGenerator()
        with pytest.raises(JsonGenerator.JsonSyntaxError):
            json_parser.parse(test_str)


def test_missing_quotes():
    test_str = (
        '{"name": "Axel, "age": 30.2, "legs": 2, "is_animal": false, "trbr": null}'
    )
    json_parser = JsonGenerator()
    with pytest.raises(JsonGenerator.JsonSyntaxError) as e:
        json_parser.parse(test_str)


def test_invalid_value():
    test_str = (
        '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": nill}'
    )
    json_parser = JsonGenerator()
    with pytest.raises(JsonGenerator.JsonSyntaxError):
        json_parser.parse(test_str)


def test_object_in_array():
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3,{"a":"b", "c":"d"}]}'
    json_parser = JsonGenerator()
    assert json_parser.parse(test_str) == json.loads(test_str)


def test_negative_numbers():
    test_str = '{"name": "Axel", "age": -30.2, "legs": -2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3,{"a":"b", "c":"d"}]}'
    json_parser = JsonGenerator()
    assert json_parser.parse(test_str) == json.loads(test_str)
