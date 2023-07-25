# lib/card.py

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


class Card:
    """
    Represents a playing card with a suit and a rank. 

    The card class provides methods for comparing cards and getting string representations of cards.
    """

    def __init__(self, suit: Suit, rank: Rank) -> None:
        """
        Initializes a card with a given suit and rank.

        :param suit: The suit of the card.
        :param rank: The rank of the card.
        :return: None
        """

        self.suit: Suit = suit
        self.rank: Rank = rank

    def __hash__(self) -> int:
        """
        Returns a hash value for a card, which is a combination of its suit and rank.

        :return: Hash value of the card.
        """

        return hash((self.suit, self.rank))

    def __eq__(self, other_card: Type['Card']) -> bool:
        """
        Checks if two cards are the same (i.e., have the same suit and rank).

        :param other_card: The other card to compare with.
        :return: True if the cards have the same suit and rank, False otherwise.
        """

        return isinstance(other_card, Card) and self.suit == other_card.suit and self.rank == other_card.rank

    def __lt__(self, other_card: Type['Card']) -> bool:
        """
        Defines the less-than ("<") operation for Card instances.

        The operation first compares the suits of the two cards. If they are different, it checks if the suit 
        of the current card is less than the other card's suit. If the suits are the same, it then checks if the 
        rank of the current card is less than the other card's rank.

        :param other_card: The other card to compare with the current card.
        :return: True if the current card should come before the other card in a sorted list, False otherwise.
        """

        if self.suit != other_card.suit:
            return self.suit.value < other_card.suit.value
        return self.rank.value < other_card.rank.value

    def __repr__(self) -> str:
        """
        Returns a string representation of the card.

        :return: String representation of the card in the format 'RANK of SUIT'.
        """

        return f"{self.rank.name} of {self.suit.name}"
