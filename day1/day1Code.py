import re

from adventOfCode2023.utils import read_input


STRING_TO_NUM = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

PATTERN_FORWARD = "|".join([key for key in STRING_TO_NUM.keys()]) + "|" + "[0-9]"
PATTERN_BACKWARD = "|".join([key[::-1] for key in STRING_TO_NUM.keys()]) + "|" + "[0-9]"


def to_int(x):
    if x.isdigit():
        return int(x)
    else:
        return STRING_TO_NUM[x]


def part1and2():
    data = read_input("day1Input.txt")

    total = 0

    for line in data:

        # forward search for the first num
        match = re.search(PATTERN_FORWARD, line)
        first_num = line[match.start():match.end()]

        # backward search from the end
        match = re.search(PATTERN_BACKWARD, line[::-1])
        last_num = line[::-1][match.start():match.end()][::-1]

        total += int(f"{to_int(first_num)}{to_int(last_num)}")

    print("Total value is {}".format(total))


if __name__ == "__main__":
    part1and2()