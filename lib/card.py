# lib/card.py

from .constants import Suit, Rank
from typing import Type


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

    def __repr__(self) -> str:
        """
        Returns a string representation of the card.

        :return: String representation of the card in the format 'RANK of SUIT'.
        """

        return f"{self.rank.name} of {self.suit.name}"
