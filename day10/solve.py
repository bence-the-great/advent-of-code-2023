from inputs import real_input, test_input_1, test_input_2  # noqa: F401


class AlreadySetException(Exception):
    pass


class Tile:
    data: str
    row: int
    col: int
    distance: int | None

    def __init__(self, data: str, row: int, col: int) -> None:
        self.data = data
        self.row = row
        self.col = col
        self.distance = None

    def __str__(self) -> str:
        return self.data

    def __repr__(self) -> str:
        return f"{self.data} ({self.row}, {self.col}) {self.distance}"

    @property
    def is_animal(self) -> bool:
        return self.data == "S"


class Matrix:
    data: list[list[Tile]]

    def __init__(self, data: list[list[Tile]]) -> None:
        self.data = data

    def __str__(self) -> str:
        return "\n".join(["".join(str(tile) for tile in row) for row in self.data])

    def get_tile(self, row: int, col: int) -> Tile:
        return self.data[row][col]

    @property
    def animal(self) -> Tile:
        for row in self.data:
            for tile in row:
                if tile.is_animal:
                    return tile

        raise Exception("Animal not found")

    def find_adjacent(self, tile: Tile) -> list[Tile]:
        adjacent: list[Tile] = []

        if tile.row >= 0:
            candidate = self.data[tile.row - 1][tile.col]
            if candidate.data in ["|", "F", "7"]:
                adjacent.append(candidate)

        if tile.col >= 0:
            candidate = self.data[tile.row][tile.col - 1]
            if candidate.data in ["-", "F", "L"]:
                adjacent.append(candidate)

        if tile.row < (len(self.data) - 1):
            candidate = self.data[tile.row + 1][tile.col]
            if candidate.data in ["|", "J", "L"]:
                adjacent.append(candidate)

        if tile.col < (len(self.data[tile.row]) - 1):
            candidate = self.data[tile.row][tile.col + 1]
            if candidate.data in ["-", "J", "7"]:
                adjacent.append(candidate)

        return adjacent

    def get_next_tiles(self, current_tiles: list[Tile]) -> list[Tile]:
        candidates: list[Tile] = []

        for current_tile in current_tiles:
            candidates += self.find_adjacent(current_tile)

        return [candidate for candidate in candidates if candidate.distance is None]


def set_distance(tiles: list[Tile], distance: int) -> bool:
    if all(tile.distance is not None for tile in tiles):
        return False

    for tile in tiles:
        if tile.distance is None:
            tile.distance = distance

    return True


def find_longest_distance(matrix: Matrix) -> int:
    animal = matrix.animal
    current_tiles = [matrix.find_adjacent(animal)[0]]
    distance = 1

    while set_distance(current_tiles, distance):
        current_tiles = matrix.get_next_tiles(current_tiles)
        distance += 1

    return distance


def parse_matrix(raw_input: str) -> Matrix:
    matrix_data: list[list[Tile]] = []

    for row, line in enumerate(raw_input.splitlines()):
        matrix_data.append([Tile(data=char, row=row, col=col) for col, char in enumerate(line)])

    return Matrix(matrix_data)


def solve(raw_input: str) -> int:
    matrix = parse_matrix(raw_input)

    return int(find_longest_distance(matrix) / 2)


if __name__ == "__main__":
    print(f"{solve(test_input_1) = }")
    print(f"{solve(test_input_2) = }")
    print(f"{solve(real_input) = }")
