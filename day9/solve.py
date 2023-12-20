from inputs import real_input, test_input  # noqa: F401


def get_next_value(values: list[int], reverse: bool) -> int:
    diffs = [values[i] - value for i, value in enumerate(values[:-1], start=1)]
    if all(value == 0 for value in diffs):
        if reverse:
            return values[-1]
        else:
            return values[0]
    else:
        if reverse:
            return values[0] - get_next_value(diffs, reverse)
        else:
            return values[-1] + get_next_value(diffs, reverse)


def solve(raw_history: str, reverse: bool) -> int:
    sum_of_next_values = 0

    for history in raw_history.splitlines():
        values = list(map(int, history.split(" ")))
        sum_of_next_values += get_next_value(values, reverse)

    return sum_of_next_values


if __name__ == "__main__":
    print(f"{solve(test_input, reverse=False) = }")
    print(f"{solve(real_input, reverse=False) = }")
    print(f"{solve(test_input, reverse=True) = }")
    print(f"{solve(real_input, reverse=True) = }")
