# Find the missing number in unsorted array of numbers between 0 and size of array
def find_missing_number(given_array: list[int]) -> int:
    return ((len(given_array) + 1) * len(given_array)) // 2 - sum(given_array)


#### Tests
assert find_missing_number([0, 4, 1, 2]) == 3
assert find_missing_number([0, 1, 2]) == 3
assert find_missing_number([3, 1, 2]) == 0

test_arr = list(range(1000))
test_arr.remove(100)
assert find_missing_number(test_arr) == 100


# missing number in range
def find_missing_range_number(given_array: list[int]) -> int:
    range_sum = sum(range(min(given_array), max(given_array) + 1))
    missing_num = range_sum - sum(given_array)
    if missing_num == 0:
        return max(given_array) + 1
    return missing_num


# TODO: missing two nums

