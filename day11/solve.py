from __future__ import annotations

import itertools

from inputs import real_input, test_input  # noqa: F401


class Galaxy:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"(x={self.x}; y={self.y})"


class Universe:
    chart: list[list[int]]
    galaxies: list[Galaxy]

    def __init__(self, raw_universe: str, expand: int) -> None:
        self.chart = []
        self.galaxies = []

        raw_universe_lines = raw_universe.splitlines()

        for line_num, line in enumerate(raw_universe_lines):
            if set(line) == {"."}:
                line_value = expand
            else:
                line_value = 1

            new_line: list[int] = []

            for col_num, char in enumerate(line):
                if char == "#":
                    self.galaxies.append(Galaxy(x=col_num, y=line_num))

                if set([universe_line[col_num] for universe_line in raw_universe_lines]) == {"."}:
                    column_value = expand
                else:
                    column_value = 1

                new_line.append(max(line_value, column_value))

            self.chart.append(new_line)

    def __str__(self) -> str:
        return "\n".join([str(row) for row in self.chart]) + "\n" + "\n".join((str(galaxy) for galaxy in self.galaxies))

    @property
    def galaxy_pairs(self) -> itertools.combinations[tuple[Galaxy, Galaxy]]:
        return itertools.combinations(self.galaxies, 2)

    def distance(self, galaxy_a: Galaxy, galaxy_b: Galaxy) -> int:
        points_horizontally = [
            c for c in self.chart[galaxy_a.y][min(galaxy_a.x, galaxy_b.x) : max(galaxy_a.x, galaxy_b.x)]
        ]
        points_vertically = [
            row[galaxy_a.x] for row in self.chart[min(galaxy_a.y, galaxy_b.y) : max(galaxy_a.y, galaxy_b.y)]
        ]

        return sum(points_horizontally + points_vertically)


def solve(universe: Universe) -> int:
    sum_distances = 0

    for galaxy_a, galaxy_b in universe.galaxy_pairs:
        sum_distances += universe.distance(galaxy_a, galaxy_b)

    return sum_distances


if __name__ == "__main__":
    print(f"{solve(Universe(raw_universe=test_input, expand=2)) = }")
    print(f"{solve(Universe(raw_universe=real_input, expand=2)) = }")
    print(f"{solve(Universe(raw_universe=test_input, expand=10)) = }")
    print(f"{solve(Universe(raw_universe=test_input, expand=100)) = }")
    print(f"{solve(Universe(raw_universe=real_input, expand=1000000)) = }")
