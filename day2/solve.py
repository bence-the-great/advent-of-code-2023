from __future__ import annotations

import re
from collections.abc import Generator

from inputs import real_input, test_input  # noqa: F401


class CubeConfiguration:
    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def copy(other: CubeConfiguration) -> CubeConfiguration:
        return CubeConfiguration(red=other.red, green=other.green, blue=other.blue)

    def __lt__(self, other: CubeConfiguration) -> bool:
        return self.red < other.red and self.green < other.green and self.blue < other.blue

    def __le__(self, other: CubeConfiguration) -> bool:
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue

    def __eq__(self, other: CubeConfiguration) -> bool:
        return self.red == other.red and self.green == other.green and self.blue == other.blue

    def __add__(self, other: CubeConfiguration) -> CubeConfiguration:
        return CubeConfiguration(
            red=max(self.red, other.red),
            green=max(self.green, other.green),
            blue=max(self.blue, other.blue),
        )

    def power(self) -> int:
        return self.red * self.green * self.blue


class Game:
    game_id: int
    sets_of_cubes: list[CubeConfiguration]

    def __init__(self, game_id: int, sets_of_cubes: list[CubeConfiguration]) -> None:
        self.game_id = game_id
        self.sets_of_cubes = sets_of_cubes

    def valid_for_bag(self, bag: CubeConfiguration) -> bool:
        return all(revealed <= bag for revealed in self.sets_of_cubes)

    def minimum_valid_bag(self) -> CubeConfiguration:
        return sum(self.sets_of_cubes, start=CubeConfiguration(0, 0, 0))


def get_cube_count(revealed_cubes: str, color: str) -> int:
    try:
        return int(re.search(f"(?P<{color}>[0-9]+) {color}", revealed_cubes).group(color))
    except AttributeError:
        return 0


def parse_revelaled_sets(raw_sets: str) -> Generator[CubeConfiguration, None, None]:
    for revealed_cubes in raw_sets.split(";"):
        yield CubeConfiguration(
            red=get_cube_count(revealed_cubes, "red"),
            green=get_cube_count(revealed_cubes, "green"),
            blue=get_cube_count(revealed_cubes, "blue"),
        )


def parser(raw_input: str) -> Generator[Game, None, None]:
    for row in raw_input.splitlines():
        game_id = int(
            re.search(
                r"Game (?P<game_id>[0-9]+)",
                row,
            ).group("game_id")
        )
        raw_sets = row.split(":")[1]
        yield Game(game_id=game_id, sets_of_cubes=list(parse_revelaled_sets(raw_sets)))


def solve_part1(raw_input: str) -> int:
    bag = CubeConfiguration(red=12, green=13, blue=14)

    return sum((game.game_id for game in parser(raw_input) if game.valid_for_bag(bag)), start=0)


def solve_part2(raw_input: str) -> int:
    return sum((game.minimum_valid_bag().power() for game in parser(raw_input)), start=0)


if __name__ == "__main__":
    print(f"{solve_part1(test_input)=}")
    print(f"{solve_part1(real_input)=}")
    print(f"{solve_part2(test_input)=}")
    print(f"{solve_part2(real_input)=}")
