# lib/player.py

import bisect
from typing import List, Type

from .card import Card


class Player:
    """
    Class representing a player in the card game. Each player has a name, a hand of cards,
    and methods to add and remove cards from the hand, check if a card is in the hand, 
    and compare players.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a player with a given name and an empty hand.

        :param name: Name of the player.
        """

        self.__name: str = name
        self.__hand: List[Card] = []

    @property
    def name(self) -> str:
        """
        Returns the player's name.

        :return: Player's name.
        """

        return self.__name

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the player's hand.

        :param card: Card to be added to the player's hand.
        """

        bisect.insort(self.__hand, card)

    def remove_card(self, card: Card) -> None:
        """
        Removes a card from the player's hand.

        :param card: Card to be removed from the player's hand.
        """

        self.__hand.remove(card)

    def has_card(self, card: Card) -> bool:
        """
        Checks if the player's hand contains a specific card.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is in the player's hand.
        """

        return card in self.__hand

    @property
    def hand(self) -> list[Card]:
        """
        Returns a copy of the player's hand.

        :return: List of Cards in player's hand.
        """

        return self.__hand.copy()

    def __eq__(self, otherPlayer: Type['Player']) -> bool:
        """
        Checks if two players are the same (i.e., have the same name).

        :param otherPlayer: Other player to be compared.
        :return: Boolean indicating whether the two players are equal.
        """

        return isinstance(otherPlayer, Player) and self.__name == otherPlayer.__name

    def __repr__(self) -> str:
        """
        Returns a string representation of the player.

        :return: String representation of the player.
        """

        return f"Player: {self.__name}, Hand: {self.__hand}"
