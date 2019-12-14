# You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

# However, they do remember a few key facts about the password:

# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same(like 22 in 122345).
# Going from left to right, the digits never decrease
# they only ever increase or stay the same(like 111123 or 135679).
# Other than the range rule, the following are true:

# 111111 meets these criteria(double 11, never decreases).
# 223450 does not meet these criteria(decreasing pair of digits 50).
# 123789 does not meet these criteria(no double).
# How many different passwords within the range given in your puzzle input meet these criteria?

# Your puzzle input is 372304-847060.

from collections import Counter

start = 372304
finish = 847060


def test_criteria(digits):
    diff = [dr - dl for dr, dl in zip(digits[1:], digits[0:-1])]
    return not any([d < 0 for d in diff]) and (any([d == 0 for d in diff]))


password_counter = 0
for num in range(start, finish+1):
    digits = [int(d) for d in str(num)]

    if test_criteria(digits):
        password_counter += 1

# print("The total number of valid passwords is: ", password_counter)

# =======================================================================================================================

# --- Part Two - --
# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

# Given this additional criterion, but still ignoring the range rule, the following are now true:

# 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
# 123444 no longer meets the criteria(the repeated 44 is part of a larger group of 444).
# 111122 meets the criteria(even though 1 is repeated more than twice, it still contains a double 22).
# How many different passwords within the range given in your puzzle input meet all of the criteria?


def additional_criteria(digits):
    diff = [dr - dl for dr, dl in zip(digits[1:], digits[0:-1])]

    diff_as_str = ""
    for d in diff:
        if d == 0:
            diff_as_str += "0"
        else:
            diff_as_str += ","
    diff_list = diff_as_str.split(",")
    return any(len(d) == 1 for d in diff_list)


password_counter = 0
for num in range(start, finish+1):
    digits = [int(d) for d in str(num)]

    if test_criteria(digits) and additional_criteria(digits):
        print(digits)
        password_counter += 1

print("The total number of valid passwords is: ", password_counter)
