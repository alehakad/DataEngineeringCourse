import re
import json
from enum import Enum
from typing import Generator, Callable, Any
from collections import namedtuple, defaultdict


# like json.loads
class JsonGenerator:
    class BoolEnum(Enum):
        false = False
        true = True

    boolean_map = {"true": BoolEnum.true, "false": BoolEnum.false}
    null_value = "null"

    class JsonSyntaxError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    @staticmethod
    def _preprocess_json(json_string: str) -> str:
        cleaned_str = ""
        inside_string = False
        for char in json_string:
            if char == '"':
                inside_string = not inside_string
            if char == " " and not inside_string:
                continue
            cleaned_str += char

        return cleaned_str

    def _split_by_first_level_comma(self, given_str: str) -> Generator[str, None, None]:
        current_token = ""
        inside_object_counter = 0
        inside_array_counter = 0
        for c in given_str:
            match c:
                case ",":
                    if not inside_object_counter and not inside_array_counter:
                        if not current_token:
                            raise JsonGenerator.JsonSyntaxError(
                                "Missing value between commas."
                            )
                        yield current_token
                        current_token = ""
                    else:
                        current_token += c
                case "{":
                    inside_object_counter += 1
                    current_token += c
                    self.bracket_stack.append("{")
                case "}":
                    inside_object_counter -= 1
                    current_token += c
                    if not self.bracket_stack or self.bracket_stack.pop() != "{":
                        raise JsonGenerator.JsonSyntaxError("Invalid object brackets")
                case "[":
                    inside_array_counter += 1
                    current_token += c
                    self.bracket_stack.append("[")

                case "]":
                    inside_array_counter -= 1
                    current_token += c
                    if not self.bracket_stack or self.bracket_stack.pop() != "[":
                        raise JsonGenerator.JsonSyntaxError("Invalid array brackets")
                case _:
                    current_token += c
        # the last token
        if current_token:
            yield current_token

    def __init__(self):
        self.bracket_stack = []

    def _parse_object(self, object_str: str):
        object_dict = {}
        if object_str[0] != "{" or object_str[-1] != "}":
            raise JsonGenerator.JsonSyntaxError("Invalid object brackets")
        object_str = object_str[1:-1]
        for json_pair in self._split_by_first_level_comma(object_str):
            if ":" not in json_pair:
                raise JsonGenerator.JsonSyntaxError("Invalid key-value pair")
            key, value = json_pair.split(":", maxsplit=1)
            if key[0] != '"' or key[-1] != '"':
                raise JsonGenerator.JsonSyntaxError("Invalid key")
            res_value = None
            # Parsing the value
            res_value = self._parse_value(value)
            object_dict[key[1:-1]] = res_value

        return object_dict

    def parse(self, json_string: str) -> dict:
        json_string = self._preprocess_json(json_string)
        return self._parse_object(json_string)

    def _parse_array(self, array_str: str) -> list:
        if array_str[0] != "[" or array_str[-1] != "]":
            raise JsonGenerator.JsonSyntaxError("Invalid array brackets")
        array_str = array_str[1:-1]
        result_array = []
        for element in self._split_by_first_level_comma(array_str):
            result_array.append(self._parse_value(element))
        return result_array

    def _parse_value(self, value: str):
        if value[0] == "{":  # Nested object
            return self._parse_object(value)
        elif value[0] == "[":  # Nested array
            return self._parse_array(value)
        elif value[0] == '"':  # String
            return value[1:-1]  # Remove quotes
        elif value in JsonGenerator.boolean_map:  # Booleans
            return JsonGenerator.BoolEnum[value].value
        elif value == JsonGenerator.null_value:  # None
            return None
        elif "." in value:  # Float
            try:
                return float(value)
            except ValueError:
                raise JsonGenerator.JsonSyntaxError(f"Invalid float value: {value}")
        else:  # Integer
            try:
                return int(value)
            except ValueError:
                raise JsonGenerator.JsonSyntaxError(f"Invalid integer value: {value}")


if __name__ == "__main__":
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null,"address": {"street": "123 Main St", "city": "Anytown", "home": 12}, "arr": [1,2,3,{"a":"b", "c":"d"}]}'
    # print(json.loads(test_str))
    json_parser = JsonGenerator()
    res_json_dict = json_parser.parse(test_str)
    print(res_json_dict)

    test_invalid_json = '{"a": "b" "c"}'
    res_json_dict = json_parser.parse(test_invalid_json)
