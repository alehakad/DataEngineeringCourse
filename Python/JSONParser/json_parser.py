import json
import re
from enum import Enum


# like json.loads
class JsonGenerator:
    class BoolEnum(Enum):
        false = False
        true = True

    boolean_map = {"true": BoolEnum.true, "false": BoolEnum.false}
    level_one_comma_split = r",(?![^{}]*\}|\[[^\]]*\])"

    def parse_object(self, object_str: str):
        object_dict = {}
        object_str = object_str.strip()[1:-1]
        for json_pair in re.split(JsonGenerator.level_one_comma_split, object_str):
            print(json_pair)
            key, value = map(str.strip, json_pair.split(":", maxsplit=1))
            res_value = None
            # Parsing the value
            res_value = self.parse_value(value)
            object_dict[key[1:-1]] = res_value

        return object_dict

    def parse(self, json_string: str) -> dict:
        return self.parse_object(json_string)

    def parse_array(self, array_str: str) -> list:
        pass

    def parse_value(self, value: str):
        # Handle different types of values
        if value[0] == "{":  # Nested object
            return self.parse_object(value)
        elif value[0] == "[":  # Nested array
            return self.parse_array(value)
        elif value[0] == '"':  # String
            return value[1:-1]  # Remove quotes
        elif value in JsonGenerator.boolean_map:  # Boolean
            return JsonGenerator.BoolEnum[value].value
        elif value == "null":  # None
            return None
        elif "." in value:  # Float
            return float(value)
        else:  # Integer
            return int(value)


if __name__ == "__main__":
    test_str = '{"name": "Axel", "age": 30.2, "legs": 2, "is_animal": false, "trbr": null, "address": {"street": "123 Main St", "city": "Anytown", "home": 12 }}'
    # print(json.loads(test_str))
    json_parser = JsonGenerator()
    print(json_parser.parse(test_str))
