from functools import partial, reduce
from typing import Callable

from inputs import real_input, test_input, test_input_part_2

ACCEPTED_WORDS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def decimal_characters_to_value(decimal_characters: str) -> int:
    return 10 * int(decimal_characters[0]) + int(decimal_characters[-1])


def fix_calibration_value_part_1(faulty_calibration_value: str) -> int:
    decimal_characters = "".join(filter(lambda char: 48 <= ord(char) <= 57, faulty_calibration_value))
    return decimal_characters_to_value(decimal_characters)


def fix_calibration_value_part_2(faulty_calibration_value: str) -> int:
    decimal_characters = ""
    for i, char in enumerate(faulty_calibration_value):
        if 48 <= ord(char) <= 57:
            decimal_characters += char
        elif faulty_calibration_value[i : i + 3] in ACCEPTED_WORDS:
            decimal_characters += str(ACCEPTED_WORDS.index(faulty_calibration_value[i : i + 3]))
        elif faulty_calibration_value[i : i + 4] in ACCEPTED_WORDS:
            decimal_characters += str(ACCEPTED_WORDS.index(faulty_calibration_value[i : i + 4]))
        elif faulty_calibration_value[i : i + 5] in ACCEPTED_WORDS:
            decimal_characters += str(ACCEPTED_WORDS.index(faulty_calibration_value[i : i + 5]))
    return decimal_characters_to_value(decimal_characters)


def add_calibration_value(
    calibration_value_sum: int, faulty_calibration_value: str, calibration_function: Callable[[str], int]
) -> int:
    return calibration_value_sum + calibration_function(faulty_calibration_value)


def solve(raw_input: str, calibration_function: Callable[[str], int]) -> int:
    return reduce(partial(add_calibration_value, calibration_function=calibration_function), raw_input.splitlines(), 0)


if __name__ == "__main__":
    print(f"{solve(test_input, fix_calibration_value_part_1)=}")
    print(f"{solve(real_input, fix_calibration_value_part_1)=}")
    print(f"{solve(test_input_part_2, fix_calibration_value_part_2)=}")
    print(f"{solve(real_input, fix_calibration_value_part_2)=}")
