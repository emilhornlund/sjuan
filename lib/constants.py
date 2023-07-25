# lib/constants.py

from enum import Enum, auto
from typing import Type


class Suit(Enum):
    """
    Enum class to represent the suit of a card. Each card suit is an auto-assigned Enum member.
    """

    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()


class Rank(Enum):
    """
    Enum class to represent the rank of a card. Each card rank is an Enum member with a 
    corresponding numerical value from 1 (Ace) to 13 (King).
    """

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

    def __lt__(self, otherRank: Type['Rank']) -> bool:
        """
        Determines if this rank is less than another rank. 
        Ranks are compared based on their numeric values.

        :param otherRank: Other rank to compare with.
        :return: Boolean indicating if this rank is less than the other rank.
        """

        return isinstance(otherRank, Rank) and self.value < otherRank.value

    def __gt__(self, otherRank: Type['Rank']) -> bool:
        """
        Determines if this rank is greater than another rank. 
        Ranks are compared based on their numeric values.

        :param otherRank: Other rank to compare with.
        :return: Boolean indicating if this rank is greater than the other rank.
        """

        return isinstance(otherRank, Rank) and self.value > otherRank.value

    def get_rank_above(self) -> Type['Rank']:
        """
        Returns the rank above the current rank. 
        If the current rank is KING, it returns KING itself as there is no rank above KING.

        :return: Rank above the current rank.
        """

        if self == Rank.KING:
            return Rank.KING

        return Rank(self.value + 1)

    def get_rank_below(self) -> Type['Rank']:
        """
        Returns the rank below the current rank. 
        If the current rank is ACE, it returns ACE itself as there is no rank below ACE.

        :return: Rank below the current rank.
        """

        if self == Rank.ACE:
            return Rank.ACE

        return Rank(self.value - 1)


class Action(Enum):
    """
    Enum class to represent the possible actions a player can take in the game. 
    Each action is an auto-assigned Enum member.
    """

    PLAY_ALL_CARDS = auto()
    PLAY_CARD = auto()
    TAKE_CARD = auto()
    GIVE_CARD = auto()
    PASS_TURN = auto()
