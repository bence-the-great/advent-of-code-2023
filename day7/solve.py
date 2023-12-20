from __future__ import annotations

from collections.abc import Generator

from inputs import real_input, test_input  # noqa: F401


class Hand:
    cards: str
    bid: int
    joker_is_active: bool

    def __init__(self, cards: str, bid: int, joker_is_active: bool) -> None:
        self.cards = cards
        self.bid = bid
        self.joker_is_active = joker_is_active

    def __str__(self) -> str:
        return f"{self.cards} {self.bid} ({self.strength})"

    @staticmethod
    def _category(cards: str) -> int:
        character_counts: dict[str, int] = {}

        for character in cards:
            character_counts[character] = len([c for c in cards if c == character])

        if len(character_counts) == 1:
            return 7
        elif [1, 4] == sorted(character_counts.values()):
            return 6
        elif [2, 3] == sorted(character_counts.values()):
            return 5
        elif [1, 1, 3] == sorted(character_counts.values()):
            return 4
        elif [1, 2, 2] == sorted(character_counts.values()):
            return 3
        elif [1, 1, 1, 2] == sorted(character_counts.values()):
            return 2
        elif len(character_counts) == 5:
            return 1

        raise Exception(f"Couldn't categorize hand {cards}")

    @property
    def strength(self) -> int:
        value: int

        if self.joker_is_active and "J" in self.cards and self.cards != "JJJJJ":
            non_joker_cards = set(self.cards.replace("J", ""))
            value = max(
                self._category(self.cards.replace("J", card)) * (16 ** len(self.cards)) for card in non_joker_cards
            )
        else:
            value = self._category(self.cards) * (16 ** len(self.cards))

        for decimal_place, character in enumerate(reversed(self.cards)):
            try:
                value += int(character) * (16**decimal_place)
            except ValueError:
                if character == "T":
                    value += 11 * (16**decimal_place)
                if character == "J":
                    if self.joker_is_active:
                        value += 1 * (16**decimal_place)
                    else:
                        value += 12 * (16**decimal_place)
                if character == "Q":
                    value += 13 * (16**decimal_place)
                if character == "K":
                    value += 14 * (16**decimal_place)
                if character == "A":
                    value += 15 * (16**decimal_place)

        return value

    def __lt__(self, other: Hand) -> bool:
        return self.strength < other.strength


def parse_hands(raw_hands: str, joker_is_active: bool) -> Generator[Hand, None, None]:
    for raw_hand in raw_hands.splitlines():
        components = raw_hand.split(" ")
        yield Hand(cards=components[0], bid=int(components[1]), joker_is_active=joker_is_active)


def solve(raw_hands: str, joker_is_active: bool) -> int:
    value = 0

    for rank, hand in enumerate(sorted(list(parse_hands(raw_hands, joker_is_active))), start=1):
        value += rank * hand.bid

    return value


if __name__ == "__main__":
    print(f"{solve(test_input, joker_is_active=False) = }")
    print(f"{solve(real_input, joker_is_active=False) = }")
    print(f"{solve(test_input, joker_is_active=True) = }")
    print(f"{solve(real_input, joker_is_active=True) = }")
