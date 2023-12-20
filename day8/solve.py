import re
from collections.abc import Callable
from functools import reduce

from inputs import real_input, test_input, test_input_2, test_input_3


class Node:
    name: str
    left: str
    right: str

    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"{self.name} = ({self.left}, {self.right})"

    def __repr__(self) -> str:
        return self.__str__()


def parse_nodes(lines: list[str]) -> dict[str, Node]:
    nodes: dict[str, Node] = {}

    for raw_node in lines:
        REGEX = r"(?P<name>[A-Z0-9]*)\s=\s[(](?P<left>[A-Z0-9]*),\s(?P<right>[A-Z0-9]*)[)]"
        match = re.match(REGEX, raw_node)

        if match is None:
            raise Exception(f"Could not parse {raw_node}")

        node = Node(**match.groupdict())

        nodes[node.name] = node

    return nodes


def calculate_rounds_to_reach_ZZZ(
    directions: str, nodes: dict[str, Node], initial_node: Node, goal_tester: Callable[[Node], bool]
) -> int:
    number_of_steps = 0
    current_node = initial_node

    while True:
        for step in directions:
            if goal_tester(current_node):
                return number_of_steps
            else:
                number_of_steps += 1

            if step == "L":
                current_node = nodes[current_node.left]
            elif step == "R":
                current_node = nodes[current_node.right]
            else:
                raise Exception(f"Unavailable step {step}")


def test_for_ZZZ(node: Node) -> bool:
    return node.name == "ZZZ"


def test_ends_in_Z(node: Node) -> bool:
    return node.name.endswith("Z")


def prime_factors(n: int) -> list[int]:
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def multiply(prime_1: int, prime_2: int) -> int:
    return prime_1 * prime_2


def solve(raw_network: str, find_nodes_simultaneously: bool) -> int:
    lines = raw_network.splitlines()
    directions = lines[0]
    nodes = parse_nodes(lines[2:])

    if find_nodes_simultaneously:
        primes: set[int] = set()
        initial_nodes = [n for _, n in nodes.items() if n.name.endswith("A")]
        for initial_node in initial_nodes:
            value = calculate_rounds_to_reach_ZZZ(directions, nodes, initial_node, test_ends_in_Z)
            for prime in prime_factors(value):
                primes.add(prime)
        return reduce(multiply, primes, 1)
    else:
        return calculate_rounds_to_reach_ZZZ(directions, nodes, nodes["AAA"], test_for_ZZZ)


if __name__ == "__main__":
    print(f"{solve(test_input, find_nodes_simultaneously=False) = }")
    print(f"{solve(test_input_2, find_nodes_simultaneously=False) = }")
    print(f"{solve(real_input, find_nodes_simultaneously=False) = }")
    print(f"{solve(test_input_3, find_nodes_simultaneously=True) = }")
    print(f"{solve(real_input, find_nodes_simultaneously=True) = }")
