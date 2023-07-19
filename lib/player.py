# lib/player.py

from typing import List

from .constants import Suit, Rank
from .card import Card


class Player:
    def __init__(self, name: str):
        """Initializes a player with a given name and an empty hand."""
        self.__name: str = name
        self.__hand: List[Card] = []

    @property
    def name(self) -> str:
        """Returns the player's name."""
        return self.__name

    def add_card(self, card: Card):
        """Adds a card to the player's hand."""
        self.__hand.append(card)

    def remove_card(self, card: Card):
        """Removes a card from the player's hand."""
        self.__hand.remove(card)

    def has_card(self, card: Card):
        """Checks if the player's hand contains a specific card."""
        return card in self.__hand

    @property
    def hand(self) -> list[Card]:
        """Returns a copy of the player's hand."""
        return self.__hand.copy()

    def __eq__(self, otherPlayer):
        """Checks if two players are the same (i.e., have the same name and the same hand)."""
        return isinstance(otherPlayer, Player) and self.__name == otherPlayer.__name

    def __repr__(self):
        """Returns a string representation of the player."""
        return f"Player: {self.__name}, Hand: {self.__hand}"
