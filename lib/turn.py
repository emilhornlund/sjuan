# lib/turn.py

from .card import Card
from .constants import Action
from .player import Player


class Turn:
    """
    Class representing a turn in the card game. It includes the actions available,
    the current player, and the valid cards that can be played.
    """

    def __init__(self, actions: list[Action], player: Player, valid_cards: list[Card]) -> None:
        """
        Constructor for the Turn class.

        :param actions: List of actions that can be performed during the turn.
        :param player: The current player.
        :param valid_cards: List of valid cards that can be played.
        """

        self.__actions: list[Action] = actions
        self.__player: Player = player
        self.__valid_cards: list[Card] = valid_cards

    @property
    def actions(self) -> list[Action]:
        """
        Get the actions that can be performed during the turn.

        :return: List of actions.
        """

        return self.__actions

    @property
    def player(self) -> Player:
        """
        Get the current player.

        :return: Current player instance.
        """

        return self.__player

    @property
    def valid_cards(self) -> list[Card]:
        """
        Get the valid cards that can be played during the turn.

        :return: List of valid cards.
        """

        return self.__valid_cards
