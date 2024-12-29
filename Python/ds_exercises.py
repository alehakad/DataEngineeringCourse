# Function that receives list a list and removes all non str objects
from collections import defaultdict
from typing import Any


def remove_non_str(objects_list: list[Any]):
    # iterate backwards not to cause iterator invalidation
    for i in range(len(objects_list) - 1, -1, -1):
        if type(objects_list[i]) != str:
            del objects_list[i]


#### Tests
obj_list = [1, 2.3, "abc", "asasa", OSError(), "aa"]
remove_non_str(obj_list)
assert len(obj_list) == 3


# Function that makes string histogram
def get_str_histogram(string: str) -> dict[str, int]:
    letters_hist = defaultdict(lambda: 0)
    for ch in string:
        letters_hist[ch] += 1

    return letters_hist


#### Tests
assert dict(sorted(get_str_histogram("Abbac").items())) == dict(sorted({'A': 1, 'b': 2, 'a': 1, 'c': 1}.items()))


# Function to find elements that are in both lists (without duplicates)
def find_list_intersection(first_list: list[Any], second_list: list[Any]) -> list[Any]:
    return list(set(first_list).intersection(set(second_list)))


#### Tests
assert sorted(find_list_intersection([1, 2, 3, 2, 4], [4, 1, 6, 7])) == sorted([1, 4])


# Function that receives dict and returns list with all unique values in dict
def get_dict_unique_values(one_dict: dict[Any, Any]) -> list[Any]:
    return list(set(one_dict.values()))


#### Tests
assert sorted(get_dict_unique_values({1: 2, 3: 2, 4: 2, 5: 1, 6: 3})) == sorted([1, 2, 3])


# Function that receives list and performs left rotation
def rotate_left(list_to_rotate: list[Any], n_rotations: int) -> list[Any]:
    n_rotations %= len(list_to_rotate)
    return list_to_rotate[n_rotations:] + list_to_rotate[:n_rotations]


#### Tests
assert rotate_left([1, 2, 3, 4, 5, 6], 0) == [1, 2, 3, 4, 5, 6]
assert rotate_left([1, 2, 3, 4, 5, 6], 4) == [5, 6, 1, 2, 3, 4]
