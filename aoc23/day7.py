from dataclasses import dataclass
from functools import total_ordering
from collections import defaultdict

CARDS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "-": 1,
}

HAND_TYPES = {"5K": 7, "4K": 6, "FH": 5, "3K": 4, "2P": 3, "1P": 2, "HC": 1}


@dataclass(frozen=True)
@total_ordering
class Card:
    label: str

    def __post_init__(self):
        assert self.label in CARDS.keys()

    def __lt__(self, other):
        return CARDS[self.label] < CARDS[other.label]

    def __repr__(self):
        return self.label


@total_ordering
@dataclass(frozen=True)
class Hand:
    hand_str: str
    joker_label: str = "-"

    def __post_init__(self):
        assert len(self.hand_str) == 5
        for c in self.hand_str:
            assert c in CARDS, "element of hand_str must be in CARDS!"
        object.__setattr__(self, "cards", [Card(i) for i in self.hand_str])
        object.__setattr__(self, "joker", Card(self.joker_label))

    @property
    def hand_type(self):
        card_count = defaultdict(int)
        num_joker = 0

        for card in self.cards:
            if card == self.joker:
                num_joker += 1
            else:
                card_count[card] += 1

        sorted_counts = sorted(card_count.values())
        if len(sorted_counts) == 0:
            return "5K"

        sorted_counts[-1] += num_joker

        match sorted_counts:
            case [5]:
                return "5K"
            case [1, 4]:
                return "4K"
            case [2, 3]:
                return "FH"
            case [1, 1, 3]:
                return "3K"
            case [1, 2, 2]:
                return "2P"
            case [1, 1, 1, 2]:
                return "1P"
            case [1, 1, 1, 1, 1]:
                return "HC"

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return HAND_TYPES[self.hand_type] < HAND_TYPES[other.hand_type]
        else:
            for card_1, card_2 in zip(self.cards, other.cards):
                match (card_1 == self.joker, card_2 == other.joker):
                    case (True, False):
                        return True
                    case (False, True):
                        return False
                    case (False, False):
                        if card_1 < card_2:
                            return True
                        elif card_1 > card_2:
                            return False
            return False

    def __eq__(self, other):
        for card_1, card_2 in zip(self.cards, other.cards):
            if card_1 == self.joker and card_2 == other.joker:
                continue
            elif card_1 != card_2:
                return False

        return True
