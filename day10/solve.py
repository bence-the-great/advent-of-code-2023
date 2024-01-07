from inputs import real_input, test_input_1, test_input_2, test_input_3, test_input_4, test_input_5


class TerminalColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class AlreadySetException(Exception):
    pass


class Tile:
    data: str
    row: int
    col: int
    distance: int | None
    _is_animal: bool

    def __init__(self, data: str, row: int, col: int) -> None:
        self.data = data
        self.row = row
        self.col = col
        self.distance = None
        self._is_animal = False

    def __str__(self) -> str:
        if self.data == "-":
            return "─"
        elif self.data == "L":
            return "└"
        elif self.data == "J":
            return "┘"
        elif self.data == "|":
            return "│"
        elif self.data == "7":
            return "┐"
        elif self.data == "F":
            return "┌"
        elif self.data == ".":
            return "."
        elif self.data == "S":
            return "▓"
        return "O"

    def __repr__(self) -> str:
        return f"{self.data} ({self.row}, {self.col}) {self.distance}"

    @property
    def is_animal(self) -> bool:
        return self._is_animal or self.data == "S"

    @property
    def is_ground(self) -> bool:
        return self.data == "."

    @property
    def is_boundary(self) -> bool:
        return self.distance is not None


class Matrix:
    data: list[list[Tile]]

    def __init__(self, data: list[list[Tile]]) -> None:
        self.data = data

    def __str__(self) -> str:
        out = ""

        for row in self.data:
            for tile in row:
                if tile.is_animal:
                    out += TerminalColors.WARNING
                    out += str(tile)
                    out += TerminalColors.ENDC
                elif not tile.is_boundary and self.is_inside(tile):
                    out += TerminalColors.OKGREEN
                    out += str(tile)
                    out += TerminalColors.ENDC
                elif tile.is_boundary:
                    out += TerminalColors.WARNING
                    out += str(tile)
                    out += TerminalColors.ENDC
                else:
                    out += str(tile)
            out += "\n"

        return out[:-1]

    def get_tile(self, row: int, col: int) -> Tile:
        return self.data[row][col]

    @property
    def animal(self) -> Tile:
        for row in self.data:
            for tile in row:
                if tile.is_animal:
                    return tile

        raise Exception("Animal not found")

    @property
    def non_boundaries(self) -> list[Tile]:
        return [tile for row in self.data for tile in row if not tile.is_boundary and not tile.is_animal]

    def find_adjacent(self, tile: Tile) -> list[Tile]:
        adjacent: list[Tile] = []

        if tile.row > 0:
            candidate = self.data[tile.row - 1][tile.col]
            if tile.data in ["S", "|", "L", "J"] and candidate.data in ["|", "F", "7"]:
                adjacent.append(candidate)

        if tile.col > 0:
            candidate = self.data[tile.row][tile.col - 1]
            if tile.data in ["S", "-", "7", "J"] and candidate.data in ["-", "F", "L"]:
                adjacent.append(candidate)

        if tile.row < (len(self.data) - 1):
            candidate = self.data[tile.row + 1][tile.col]
            if tile.data in ["S", "|", "7", "F"] and candidate.data in ["|", "J", "L"]:
                adjacent.append(candidate)

        if tile.col < (len(self.data[tile.row]) - 1):
            candidate = self.data[tile.row][tile.col + 1]
            if tile.data in ["S", "-", "L", "F"] and candidate.data in ["-", "J", "7"]:
                adjacent.append(candidate)

        return adjacent

    def get_next_tiles(self, current_tiles: list[Tile]) -> list[Tile]:
        candidates: list[Tile] = []

        for current_tile in current_tiles:
            candidates += self.find_adjacent(current_tile)

        return [candidate for candidate in candidates if candidate.distance is None]

    def is_inside(self, tile: Tile) -> True:
        previous_boundaries_in_row = [
            other_tile for other_tile in self.data[tile.row][: tile.col + 1] if other_tile.is_boundary
        ]

        inside = False
        last_boundary = ""

        for b in previous_boundaries_in_row:
            if b.data in ["|", "L", "F"]:
                inside = not inside
                last_boundary = b.data
            elif b.data == "7" and last_boundary == "F":
                inside = not inside
                last_boundary = b.data
            elif b.data == "J" and last_boundary == "L":
                inside = not inside
                last_boundary = b.data

        return inside

    def fix_animal(self) -> None:
        animal = self.animal
        a = self.find_adjacent(animal)[0]
        b = self.find_adjacent(animal)[1]

        if a.row < animal.row:
            if b.col < animal.col:
                animal.data = "J"
            elif b.col > animal.col:
                animal.data = "L"
            elif b.row > animal.row:
                animal.data = "|"
        elif a.row > animal.row:
            if b.col < animal.col:
                animal.data = "7"
            elif b.col > animal.col:
                animal.data = "F"
            elif b.row < animal.row:
                animal.data = "|"
        elif a.col < animal.col:
            if b.col > animal.col:
                animal.data = "-"
            elif b.row < animal.row:
                animal.data = "J"
            elif b.row > animal.row:
                animal.data = "7"
        elif a.col > animal.col:
            if b.col < animal.col:
                animal.data = "-"
            elif b.row < animal.row:
                animal.data = "L"
            elif b.row > animal.row:
                animal.data = "F"

        animal.distance = 0
        animal._is_animal = True


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

    return int(distance / 2)


def parse_matrix(raw_input: str) -> Matrix:
    matrix_data: list[list[Tile]] = []

    for row, line in enumerate(raw_input.splitlines()):
        matrix_data.append([Tile(data=char, row=row, col=col) for col, char in enumerate(line)])

    return Matrix(matrix_data)


def solve(raw_input: str) -> tuple[int, int]:
    matrix = parse_matrix(raw_input)

    longest_distance = find_longest_distance(matrix)

    matrix.fix_animal()

    ground_indside = len([ground for ground in matrix.non_boundaries if matrix.is_inside(ground)])

    return longest_distance, ground_indside


if __name__ == "__main__":
    print(f"{solve(test_input_1) = }")
    print(f"{solve(test_input_2) = }")
    print(f"{solve(test_input_3) = }")
    print(f"{solve(test_input_4) = }")
    print(f"{solve(test_input_5) = }")
    print(f"{solve(real_input) = }")
