# lib/deck.py

import random
from .constants import Suit, Rank
from .card import Card


class Deck:
    def __init__(self):
        """Initializes a deck with a standard set of 52 cards."""
        self.__cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    @property
    def cards(self) -> list[Card]:
        """Returns a copy of the cards in the deck."""
        return self.__cards.copy()

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self.__cards)

    def deal(self) -> Card:
        """Removes and returns a card from the deck. The card is removed from the end."""
        if len(self.__cards) == 0:
            raise ValueError("Cannot deal from an empty deck.")
        return self.__cards.pop()

    def __repr__(self):
        """Returns a string representation of the deck, showing the number of cards."""
        return f"Deck of {len(self.__cards)} cards"
