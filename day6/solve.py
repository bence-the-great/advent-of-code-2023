from collections.abc import Callable, Generator

from inputs import real_input, test_input  # noqa: F401


class Race:
    time_available: int
    record: int

    def __init__(self, time_available: int, record: int) -> None:
        self.time_available = time_available
        self.record = record

    def __str__(self) -> str:
        return f"{self.time_available} {self.record}"

    @property
    def ways_to_beat(self) -> int:
        succesful_attempts = 0
        for velocity in range(self.time_available):
            distance = velocity * (self.time_available - velocity)
            if distance > self.record:
                succesful_attempts += 1
        return succesful_attempts


def parse_races(raw_races: str) -> Generator[Race, None, None]:
    lines = raw_races.splitlines()
    times = list(map(int, lines[0].split(":")[1].strip().split()))
    distances = list(map(int, lines[1].split(":")[1].strip().split()))

    for time_available, record in zip(times, distances):
        yield Race(time_available, record)


def parse_as_single_race(raw_races: str) -> Generator[Race, None, None]:
    lines = raw_races.splitlines()
    time_available = int(lines[0].split(":")[1].replace(" ", ""))
    record = int(lines[1].split(":")[1].replace(" ", ""))

    yield Race(time_available, record)


def solve(raw_races: str, parser: Callable[[str], Generator[Race, None, None]]) -> int:
    product = 1

    for race in parser(raw_races):
        product *= race.ways_to_beat

    return product


if __name__ == "__main__":
    print(f"{solve(test_input, parser=parse_races) = }")
    print(f"{solve(real_input, parser=parse_races) = }")
    print(f"{solve(test_input, parser=parse_as_single_race) = }")
    print(f"{solve(real_input, parser=parse_as_single_race) = }")
