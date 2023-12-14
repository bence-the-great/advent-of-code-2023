import re
from collections.abc import Generator
from functools import cached_property

from inputs import real_input, test_input  # noqa: F401


class Card:
    game_id: int
    winning_numbers: list[int]
    guessed_numbers: list[int]
    copies: int

    def __init__(self, game_id: int, winning_numbers: list[int], guessed_numbers: list[int]) -> None:
        self.game_id = game_id
        self.winning_numbers = winning_numbers
        self.guessed_numbers = guessed_numbers
        self.copies = 1

    def __str__(self) -> str:
        winning_numbers = " ".join(f"{number:2d}" for number in self.winning_numbers)
        guessed_numbers = " ".join(f"{number:2d}" for number in self.guessed_numbers)
        return f"Game {self.game_id}: {winning_numbers} | {guessed_numbers}"

    @cached_property
    def matches(self) -> int:
        return len(set(self.winning_numbers).intersection(set(self.guessed_numbers)))

    def points(self) -> int:
        if self.matches <= 0:
            return 0
        else:
            power = self.matches - 1
            return 2**power  # type: ignore


def parse_game_id(raw_card: str) -> int:
    regex_match = re.search("Card[\s]*(?P<game_id>[0-9]+)", raw_card)
    if regex_match is None:
        raise Exception(f"No game id found. {raw_card=}")
    else:
        return int(regex_match.group("game_id"))


def parse_winning_numbers(raw_card: str) -> list[int]:
    raw_numbers = re.findall(r"\d+", raw_card.split(":")[1].split("|")[0])
    return list(map(int, raw_numbers))


def parse_guessed_numbers(raw_card: str) -> list[int]:
    raw_numbers = re.findall(r"\d+", raw_card.split(":")[1].split("|")[1])
    return list(map(int, raw_numbers))


def parse_cards(raw_cards: str) -> Generator[Card, None, None]:
    for raw_card in raw_cards.splitlines():
        yield Card(
            game_id=parse_game_id(raw_card),
            winning_numbers=parse_winning_numbers(raw_card),
            guessed_numbers=parse_guessed_numbers(raw_card),
        )


def count_points_scored(raw_cards: str) -> int:
    return sum(card.points() for card in parse_cards(raw_cards))


def count_scratchcards(raw_cards: str) -> int:
    cards = list(parse_cards(raw_cards))

    for card_id, card in enumerate(cards):
        for i in range(1, card.matches + 1):
            cards[card_id + i].copies += card.copies

    return sum(card.copies for card in cards)


if __name__ == "__main__":
    print(f"{count_points_scored(test_input) = }")
    print(f"{count_points_scored(real_input) = }")
    print(f"{count_scratchcards(test_input) = }")
    print(f"{count_scratchcards(real_input) = }")
