## Python exercises


### Function that returns number of times a character appears in string
def count_char_occurrences(string: str, char: str) -> int:
    """
    Count the number of occurrences of certain character in a string.
    """
    return string.count(char)


def count_char_occurrences2(string: str, char: str) -> int:
    """
    Count the number of occurrences of certain character in a string.
    """
    counter = 0
    for c in string:
        if c == char:
            counter += 1

    return counter


#### Tests
print(count_char_occurrences2("blablabla a", "a") == count_char_occurrences("blablabla a", "a"))
print(count_char_occurrences2("abcdefg", "z") == count_char_occurrences("abcdefg", "z"))
print(count_char_occurrences2("123 b a", "3") == count_char_occurrences("123 b a", "3"))


### Function that flips a number
def flip_number(num: int | float) -> float:
    if num < 0:
        return float(str(num)[1::][::-1]) * -1
    return float(str(num)[::-1])


#### Tests
assert (flip_number(1234) == 4321)
assert (flip_number(0) == 0)
assert (flip_number(1.2) == 2.1)
assert (flip_number(-34) == -43)


### Celsius to Fahrenheit
def convert_celsius_to_fahrenheit(temperature: float) -> float:
    return temperature * 9 / 5 + 32


#### Tests
assert (convert_celsius_to_fahrenheit(233) == 451.4)
assert (convert_celsius_to_fahrenheit(-100) == -148)
assert (convert_celsius_to_fahrenheit(0) == 32)


#### Leap year checking function
def is_leap_year(year: int) -> bool:
    return not year % 4 and (year % 100 or not year % 400)


#### Tests
assert (is_leap_year(2024))
assert (not is_leap_year(2023))
assert (not is_leap_year(300))
assert (is_leap_year(1600))


### Check password complexity:
# - \>=  8 chars
# - Latin letters in both upper and lower case
# - numbers from 0 to 9
# - contains at least one @, #, %, &

def check_password(password: str) -> bool:
    if len(password) < 8:
        return False
    contains_num, contains_cap_letter, contains_low_letter, contains_special_char = False, False, False, False
    for c in password:
        if c.isalpha():
            if c.isupper():
                contains_cap_letter = True
            elif c.islower():
                contains_low_letter = True
        elif c.isdigit():
            contains_num = True
        elif c in {'@', '#', '%', '&'}:
            contains_special_char = True

    return contains_num and contains_cap_letter and contains_low_letter and contains_special_char


#### Tests
assert not check_password("123BlaBla")
assert check_password("123@BlaBla")


# Function to return sum of number divisors
def count_divisors_sum(number: int) -> int:
    total_sum = 0
    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            total_sum += i
            if i != number // i:
                total_sum += number // i

    return total_sum


#### Tests
assert count_divisors_sum(2) == 3
assert count_divisors_sum(1) == 1
assert count_divisors_sum(28) == 56


# Function that splits amount of money to banknotes and coins
# banknotes are 20, 50, 100, 200
# coins are 1, 2, 5, 10
# minimum number of bills and coins
def split_money(amount: int) -> dict[int, int]:
    amounts = [1, 2, 5, 10, 20, 50, 100, 200]
    res_amounts_map = {b: 0 for b in amounts}
    dp_res = [(float('inf'), []) for _ in range(amount + 1)]
    dp_res[0] = (0, [])
    for b in amounts:
        dp_res[b] = (1, [b])
    for i in range(1, amount + 1):
        for b in amounts:
            if i - b >= 0:
                coins_used = dp_res[i - b][0] + 1
                if coins_used < dp_res[i][0]:
                    dp_res[i] = (coins_used, dp_res[i - b][1] + [b])
    for b in dp_res[amount][1]:
        res_amounts_map[b] += 1

    return res_amounts_map


# Tests
assert split_money(234) == {200: 1, 100: 0, 50: 0, 20: 1, 10: 1, 5: 0, 2: 2, 1: 0}


# Function that checks that the number is prime
def is_prime_number(number: int) -> bool:
    if number == 1: return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


# Tests
assert is_prime_number(2)
assert not is_prime_number(1)
assert is_prime_number(3)
assert not is_prime_number(4)
assert is_prime_number(131)
