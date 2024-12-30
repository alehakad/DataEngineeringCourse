# Function that removes specific words from given list
def remove_words(lst: list[str], word_list: set[str]):
    return list(filter(lambda wrd: wrd not in word_list, lst))


#### Tests
def test_remove_words():
    # Test with no words to remove
    initial_list = ["apple", "banana", "cherry"]
    words_to_remove = set()
    assert remove_words(initial_list, words_to_remove) == ["apple", "banana", "cherry"]

    # Test with all words to remove
    initial_list = ["apple", "banana", "cherry"]
    words_to_remove = {"apple", "banana", "cherry"}
    assert remove_words(initial_list, words_to_remove) == []

    # Test with some words to remove
    initial_list = ["apple", "banana", "cherry", "date"]
    words_to_remove = {"banana", "date"}
    assert remove_words(initial_list, words_to_remove) == ["apple", "cherry"]

    # Test with repeated words in the list
    initial_list = ["apple", "banana", "apple", "cherry", "banana"]
    words_to_remove = {"banana"}
    assert remove_words(initial_list, words_to_remove) == ["apple", "apple", "cherry"]

    # Test with empty list
    initial_list = []
    words_to_remove = {"apple", "banana"}
    assert remove_words(initial_list, words_to_remove) == []

    # Test with empty set and empty list
    initial_list = []
    words_to_remove = set()
    assert remove_words(initial_list, words_to_remove) == []

# Run the tests
test_remove_words()
print("All tests passed.")

# Function to sort list of strings(numbers) numerically
def sort_numerically(lst: list[str]) -> list[str]:
    return sorted(lst, key=lambda x: int(x))

#### Tests
def test_sort_numerically():
    # Test with an empty list
    initial_list = []
    assert sort_numerically(initial_list) == []

    # Test with a single number
    initial_list = ["5"]
    assert sort_numerically(initial_list) == ["5"]

    # Test with positive numbers
    initial_list = ["10", "2", "7", "1", "3"]
    assert sort_numerically(initial_list) == ["1", "2", "3", "7", "10"]

    # Test with negative numbers
    initial_list = ["-5", "-2", "-7", "-1", "-3"]
    assert sort_numerically(initial_list) == ["-7", "-5", "-3", "-2", "-1"]

    # Test with mixed positive and negative numbers
    initial_list = ["-10", "5", "-2", "7", "-1", "3"]
    assert sort_numerically(initial_list) == ["-10", "-2", "-1", "3", "5", "7"]


# Run the tests
test_sort_numerically()
print("All tests passed.")

# Function to calculate the sum of positive and negative numbers in a list
def calculate_pos_neg_sum(lst: list[int]) -> tuple[int, int]:
    pos_sum = sum(filter(lambda x: x > 0, lst))
    neg_sum = sum(filter(lambda x: x < 0, lst))

    return pos_sum, neg_sum

#### Tests
def test_calculate_pos_neg_sum():
    # Test with an empty list
    initial_list = []
    assert calculate_pos_neg_sum(initial_list) == (0, 0)

    # Test with positive numbers only
    initial_list = [1, 2, 3, 4, 5]
    assert calculate_pos_neg_sum(initial_list) == (15, 0)

    # Test with negative numbers only
    initial_list = [-1, -2, -3, -4, -5]
    assert calculate_pos_neg_sum(initial_list) == (0, -15)

    # Test with mixed positive and negative numbers
    initial_list = [-1, 2, -3, 4, -5]
    assert calculate_pos_neg_sum(initial_list) == (6, -9)

    # Test with zero
    initial_list = [0, 0, 0, 0]
    assert calculate_pos_neg_sum(initial_list) == (0, 0)

    # Test with repeated numbers
    initial_list = [1, 1, 1, -1, -1, -1]
    assert calculate_pos_neg_sum(initial_list) == (3, -3)

# Run the tests
test_calculate_pos_neg_sum()
print("All tests passed.")


# Function to construct list of squares of list elements
def square_elements(lst: list[int]) -> list[int]:
    return [num**2 for num in lst if num%2 == 0]

#### Tests
def test_square_elements():
    initial_list = [1,2,3,4]
    assert square_elements(initial_list) == [4, 16]

test_square_elements()
print("All tests passed.")


# Function that returns dict with 10% sale price values
def get_percentaged_list(lst: dict[str, float]) -> dict[str, float]:
    return {key: value*0.1 for key, value in lst.items()}


#### Tests
def test_get_percentaged_list():
    # Test Case: Typical input with several values
    input_data = {"a": 100.0, "b": 50.0, "c": 25.0}
    expected_output = {"a": 10.0, "b": 5.0, "c": 2.5}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 1 Failed"

    # Test Case: Empty dictionary
    input_data = {}
    expected_output = {}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 2 Failed"

    # Test Case: Single element in dictionary
    input_data = {"x": 200.0}
    expected_output = {"x": 20.0}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 3 Failed"

    # Test Case: All values are zero
    input_data = {"a": 0.0, "b": 0.0, "c": 0.0}
    expected_output = {"a": 0.0, "b": 0.0, "c": 0.0}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 4 Failed"

    # Test Case: Negative values in dictionary
    input_data = {"a": -100.0, "b": -50.0, "c": -25.0}
    expected_output = {"a": -10.0, "b": -5.0, "c": -2.5}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 5 Failed"

    # Test Case: Large values
    input_data = {"a": 1000000.0, "b": 500000.0}
    expected_output = {"a": 100000.0, "b": 50000.0}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 6 Failed"

    # Test Case: Very small numbers (close to zero but positive)
    input_data = {"a": 0.0001, "b": 0.0005}
    expected_output = {"a": 0.00001, "b": 0.00005}
    assert get_percentaged_list(input_data) == expected_output, "Test Case 7 Failed"


# Run the tests
test_get_percentaged_list()
print("All tests passed")



# changing nonlocal variable
def outer_func():
    x = 4
    def inner_func():
        nonlocal x
        x = 3
    inner_func()
    print(x)

outer_func()

