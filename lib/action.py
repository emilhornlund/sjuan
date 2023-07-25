# lib/action.py

from enum import Enum, auto
from typing import Optional, Type

from lib.card import Card


class ActionType(Enum):
    """
    Enum class to represent the possible action types a player can take in the game. 
    Each action is an auto-assigned Enum member.
    """

    PLAY_ALL_CARDS = auto()
    PLAY_CARD = auto()
    TAKE_CARD = auto()
    GIVE_CARD = auto()
    PASS_TURN = auto()


class Action:
    """
    This class represents an action in the game.

    Each action has a type, defined by the ActionType Enum, 
    and optionally has an associated card.
    """

    def __init__(self, type: ActionType, card: Optional[Card] = None) -> None:
        """
        Initialize an Action instance.

        :param type: ActionType, the type of the action.
        :param card: Card, the card associated with the action.
        """

        self.__type = type
        self.__card = card

    @property
    def type(self) -> ActionType:
        """
        Property to get the type of the action.

        :return: ActionType, the type of the action.
        """

        return self.__type

    @property
    def card(self) -> Optional[Card]:
        """
        Property to get the card associated with the action.

        :return: Card or None, the card associated with the action, if any.
        """

        return self.__card

    def __eq__(self, other_action: 'Action') -> bool:
        """
        Determines if this action is equal to another action.

        Two actions are equal if they are of the same type and have the same associated card.

        :param other_action: Action, the other action to compare with.
        :return: bool, True if actions are equal, False otherwise.
        """

        return isinstance(other_action, Action) and self.type == other_action.type and self.card == other_action.card

    def __hash__(self) -> int:
        """
        Calculates the hash of the action.

        The hash is calculated based on the action type and the associated card.

        :return: int, the hash of the action.
        """

        return hash((self.type, self.card))

    def __str__(self) -> str:
        """
        Returns a string representation of the action.

        The string representation depends on the type of the action and the associated card, if any.

        :return: str, the string representation of the action.
        """

        if self.__type is ActionType.PLAY_ALL_CARDS:
            return "Play all cards"
        elif self.__type is ActionType.PLAY_CARD:
            return f"Play {self.__card}"
        elif self.__type is ActionType.TAKE_CARD:
            return "Take card"
        elif self.__type is ActionType.GIVE_CARD:
            return f"Give {self.__card}"
        elif self.__type is ActionType.PASS_TURN:
            return "Pass turn"
