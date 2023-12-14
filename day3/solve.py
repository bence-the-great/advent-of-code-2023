from __future__ import annotations

from collections.abc import Generator

from inputs import real_input, test_input  # noqa: F401

SYMBOLS = {
    ":",
    "^",
    "_",
    "`",
    ",",
    ";",
    "<",
    "(",
    "@",
    "*",
    "=",
    "~",
    ">",
    '"',
    "]",
    "{",
    ")",
    "%",
    " ",
    "+",
    "/",
    "$",
    "\\",
    "[",
    "-",
    "!",
    "|",
    "'",
    "#",
    "?",
    "&",
    "}",
}


class Position:
    row: int
    col: int

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"{self.row};{self.col}"

    def adjacent_numbers(self, numbers: list[Number]) -> list[Number]:
        return [number for number in numbers if number.has_adjacent_symbol(symbols=[self])]


class Number:
    value: int
    start: Position
    end: Position

    def __init__(self, value: int, start: Position, end: Position) -> None:
        self.value = value
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"{self.value} ({self.start} -> {self.end})"

    def has_adjacent_symbol(self, symbols: list[Position]) -> bool:
        for symbol in symbols:
            if abs(symbol.row - self.start.row) <= 1 and ((self.start.col - 1) <= symbol.col <= (self.end.col + 1)):
                return True
        return False


def is_number(character: str) -> bool:
    return 48 <= ord(character) <= 57


def end_of_the_row(row: str, current_col: int) -> bool:
    return len(row) == (current_col + 1)


def parse_numbers(raw_input: str) -> Generator[Number, None, None]:
    schematic = raw_input.splitlines()
    for current_row, row in enumerate(schematic):
        current_number_value = ""
        start_col = None
        for current_col in range(len(row)):
            if is_number(schematic[current_row][current_col]):
                if start_col is None:
                    start_col = current_col
                current_number_value += schematic[current_row][current_col]
                if end_of_the_row(row, current_col) or not is_number(schematic[current_row][current_col + 1]):
                    yield Number(
                        value=int(current_number_value),
                        start=Position(row=current_row, col=start_col),
                        end=Position(row=current_row, col=current_col),
                    )
                    current_number_value = ""
                    start_col = None


def parse_symbols(raw_input: str, accepted_symbols: set[str]) -> Generator[Position, None, None]:
    schematic = raw_input.splitlines()
    for current_row, row in enumerate(schematic):
        for current_col in range(len(row)):
            if schematic[current_row][current_col] in accepted_symbols:
                yield Position(row=current_row, col=current_col)


def count_part_numbers(raw_input: str) -> int:
    numbers = list(parse_numbers(raw_input))
    symbols = list(parse_symbols(raw_input, accepted_symbols=SYMBOLS))

    return sum((number.value for number in numbers if number.has_adjacent_symbol(symbols)))


def count_gear_ratios(raw_input: str) -> int:
    numbers = list(parse_numbers(raw_input))
    symbols = list(parse_symbols(raw_input, accepted_symbols={"*"}))

    result = 0

    for symbol in symbols:
        adjacent = symbol.adjacent_numbers(numbers)
        if len(adjacent) == 2:
            result += adjacent[0].value * adjacent[1].value

    return result


if __name__ == "__main__":
    print(f"{count_part_numbers(test_input)= }")
    print(f"{count_part_numbers(real_input)= }")
    print(f"{count_gear_ratios(test_input)= }")
    print(f"{count_gear_ratios(real_input)= }")
