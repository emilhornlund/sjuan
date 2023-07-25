# lib/deck.py

import random
from .constants import Suit, Rank
from .card import Card


class Deck:
    """
    Class representing a deck of cards in the card game. Each deck has 52 cards, 
    one for each suit and rank combination. The deck can be shuffled, a card can 
    be dealt from it, and it can be checked whether it is empty.
    """

    def __init__(self) -> None:
        """
        Initializes a deck with a standard set of 52 cards.

        :return: None
        """

        self.__cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    @property
    def cards(self) -> list[Card]:
        """
        Returns a copy of the cards in the deck.

        :return: List of Cards in the deck.
        """

        return self.__cards.copy()

    def shuffle(self) -> None:
        """
        Shuffles the deck in place using the random.shuffle method.

        :return: None
        """

        random.shuffle(self.__cards)

    def deal(self) -> Card:
        """
        Removes and returns a card from the deck. The card is removed from the end.
        Raises a ValueError if the deck is empty.

        :return: Card dealt from the deck.
        """

        if len(self.__cards) == 0:
            raise ValueError("Cannot deal from an empty deck.")

        return self.__cards.pop()

    def empty(self) -> bool:
        """
        Determines whether the deck is empty or not.

        :return: Boolean indicating whether the deck is empty.
        """

        return len(self.__cards) == 0

    def __repr__(self) -> str:
        """
        Returns a string representation of the deck, showing the number of cards.

        :return: String representation of the deck.
        """

        return f"Deck of {len(self.__cards)} cards"
