# lib/constants.py

from enum import Enum, auto


class Suit(Enum):
    """Enum class to represent the suit of a card."""
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()


class Rank(Enum):
    """Enum class to represent the rank of a card."""
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __lt__(self, otherRank):
        """Determines if this rank is less than another rank. 
        Ranks are compared based on their numeric values.
        """
        return isinstance(otherRank, Rank) and self.value < otherRank.value

    def __gt__(self, otherRank):
        """Determines if this rank is greater than another rank. 
        Ranks are compared based on their numeric values.
        """
        return isinstance(otherRank, Rank) and self.value > otherRank.value

    def get_rank_above(self):
        """Returns the rank above the current rank. 
        If the current rank is KING, it returns KING itself as there is no rank above KING.
        """
        if self == Rank.KING:
            return Rank.KING
        return Rank(self.value + 1)

    def get_rank_bellow(self):
        """Returns the rank below the current rank. 
        If the current rank is ACE, it returns ACE itself as there is no rank below ACE.
        """
        if self == Rank.ACE:
            return Rank.ACE
        return Rank(self.value - 1)
