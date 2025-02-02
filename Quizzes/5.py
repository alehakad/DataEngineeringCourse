# Write a python function that gets a number, and replaces one of the digits with a '5' to achieve the highest number.
def replace_with_five(num:int):
    str_num = str(num)
    for i in range(len(str_num)):
        if int(str_num[i]) < 5:
            return int(str_num[:i] + '5' + str_num[i+1:])
    return int(str_num[:-1] + '5')
# test
assert replace_with_five(123) == 523
assert replace_with_five(1234) == 5234
assert replace_with_five(12345) == 52345
assert replace_with_five(8974) == 8975
assert replace_with_five(7615) == 7655
assert replace_with_five(6789) == 6785 