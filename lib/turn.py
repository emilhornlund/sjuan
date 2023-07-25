# lib/turn.py

from typing import Set

from .action import Action
from .player import Player


class Turn:
    """
    Class representing a turn in the card game. It includes the actions available and
    the current player.
    """

    def __init__(self, actions: Set[Action], player: Player) -> None:
        """
        Constructor for the Turn class.

        :param actions: Set of actions that can be performed during the turn.
        :param player: The current player.
        :return: None
        """

        self.__actions: Set[Action] = actions
        self.__player: Player = player

    @property
    def actions(self) -> Set[Action]:
        """
        Get the actions that can be performed during the turn.

        :return: Set of actions.
        """

        return self.__actions

    @property
    def player(self) -> Player:
        """
        Get the current player.

        :return: Current player instance.
        """

        return self.__player

    def has_action(self, action: Action) -> bool:
        """
        Check if a particular action is available in the current turn.

        :param action: The action to check.
        :return: True if the action is available, False otherwise.
        """

        return any(__action == action for __action in self.__actions)
