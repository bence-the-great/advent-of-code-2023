from __future__ import annotations

from functools import reduce

from inputs import real_input, test_input  # noqa: F401


class Range:
    destination_start: int
    source_start: int
    length: int

    def __init__(self, destination_start: int, source_start: int, length: int) -> None:
        self.destination_start = destination_start
        self.source_start = source_start
        self.length = length

    def __str__(self) -> str:
        return f"{self.destination_start} {self.source_start} {self.length}"

    @staticmethod
    def parse(raw_range: str) -> Range:
        range_split = raw_range.split(" ")
        return Range(
            destination_start=int(range_split[0]),
            source_start=int(range_split[1]),
            length=int(range_split[2]),
        )


def parse_ranges(raw_ranges: list[str]) -> list[Range]:
    return [Range.parse(raw_range) for raw_range in raw_ranges]


class Map:
    name: str
    ranges: list[Range]

    def __init__(self, name: str, ranges: list[Range]) -> None:
        self.name = name
        self.ranges = ranges

    def __str__(self) -> str:
        return f"{self.name}:" + "\n" + "\n".join(str(conversion_range) for conversion_range in self.ranges) + "\n"

    def convert(self, value: int) -> int:
        for conversion_range in self.ranges:
            delta = value - conversion_range.source_start
            if 0 <= delta <= conversion_range.length:
                return conversion_range.destination_start + delta

        return value

    def get_seed(self, value: int) -> int:
        for conversion_range in self.ranges:
            delta = value - conversion_range.destination_start
            if 0 <= delta <= conversion_range.length:
                return conversion_range.source_start + delta

        return value


def parse_maps(lines: list[str]) -> list[Map]:
    maps: list[Map] = []

    current_map_name = None
    current_map_start = None

    for line_number, line in enumerate(lines):
        if ":" in line:
            current_map_name = line.split(":")[0]
            current_map_start = line_number + 1
        if len(line) == 0:
            if current_map_name is None:
                raise Exception(f"{current_map_name=} at {line_number=}")
            if current_map_start is None:
                raise Exception(f"{current_map_start=} at {line_number=}")
            maps.append(Map(name=current_map_name, ranges=parse_ranges(lines[current_map_start:line_number])))
            current_map_name = None
            current_map_start = None

    if current_map_name is None:
        raise Exception(f"{current_map_name=} at {line_number=}")
    if current_map_start is None:
        raise Exception(f"{current_map_start=} at {line_number=}")
    maps.append(Map(name=current_map_name, ranges=parse_ranges(lines[current_map_start : len(lines)])))

    return maps


def convert_value(value: int, conversion_map: Map) -> int:
    return conversion_map.convert(value)


def get_seed(value: int, conversion_map: Map) -> int:
    return conversion_map.get_seed(value)


def calculate_minimum_location(raw_maps: str) -> int:
    lines = raw_maps.splitlines()
    seeds = list(map(int, lines[0].split(":")[1].strip(" ").split(" ")))
    maps = parse_maps(lines[2:])

    values = [reduce(convert_value, maps, seed) for seed in seeds]

    return min(values)


def calculte_with_seed_ranges(raw_maps: str, increments: int = 1) -> int:
    lines = raw_maps.splitlines()
    raw_seeds = list(map(int, lines[0].split(":")[1].strip(" ").split(" ")))
    pairs = list(zip(raw_seeds[::2], raw_seeds[1::2]))
    maps = list(reversed(parse_maps(lines[2:])))

    current_location = 0
    while True:
        seed = reduce(get_seed, maps, current_location)
        for seed_range_start, seed_range_length in pairs:
            delta = seed - seed_range_start
            if 0 <= delta <= seed_range_length:
                if increments > 1:
                    current_location -= increments
                    increments = 1
                else:
                    return current_location
        current_location += increments


if __name__ == "__main__":
    print(f"{calculate_minimum_location(test_input) = }")
    print(f"{calculate_minimum_location(real_input) = }")
    print(f"{calculte_with_seed_ranges(test_input) = }")
    print(f"{calculte_with_seed_ranges(real_input, increments=10000) = }")
