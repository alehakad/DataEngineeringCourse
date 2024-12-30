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


# Function that removes and prints every second number from list until it becomes empty
def print_even_elements(list_to_print: list[int]) -> None:
    temp_list = []
    while len(list_to_print) >= 2:
        for i in range(len(list_to_print)):
            if i % 2 == 1:
                print(list_to_print[i])
            else:
                temp_list.append(list_to_print[i])

        list_to_print = temp_list
        temp_list = []


#### Tests
print_even_elements(list(range(10)))


# Function to convert dictionary ot list of tuples
def convert_dict_to_tuples_list(given_dict: dict[Any, Any]) -> list[tuple[Any, Any]]:
    return list(given_dict.items())


#### Tests
assert convert_dict_to_tuples_list({1: 2, 3: 4, 5: 4}) == [(1, 2), (3, 4), (5, 4)]


# Function to find max and min values in dict and print keys
def find_max_min_values_keys(given_dict: dict[int, int]) -> None:
    max_key, min_key = None, None
    max_val, min_val = float('-inf'), float('inf')
    for key, val in given_dict.items():
        if val > max_val:
            max_val = val
            max_key = key
        if val < min_val:
            min_val = val
            min_key = key

    print(min_key, max_key)


#### Tests
find_max_min_values_keys({1: 2, 3: 4, 5: 6, -1: -10})
