import random
from typing import List, NamedTuple

from lib.card import Card
from lib.constants import Action
from lib.turn import Turn


class AIMove(NamedTuple):
    """
    Represents a move made by the AI player.
    """

    action: Action
    card: Card


class AIPlayer:
    """
    AI Player class responsible for making moves for the AI player in the game.
    """

    @staticmethod
    def play_turn(board_matrix: List[List[bool]], turn: Turn) -> AIMove:
        """
        Generate and return a move for the AI player in the given turn.

        :param board_matrix: The current state of the game board represented as a matrix of boolean values.
        :param turn: The current turn object containing available actions and valid cards for the AI player.
        :return: An AIMove object representing the AI player's move (action and card choice).
        """

        action_choice: Action = random.choice(turn.actions)
        if action_choice is Action.PLAY_ALL_CARDS:
            return AIMove(action=Action.PLAY_ALL_CARDS, card=None)
        elif action_choice is Action.PLAY_CARD:
            card_choice = random.choice(turn.valid_cards)
            return AIMove(action=Action.PLAY_CARD, card=card_choice)
        elif action_choice is Action.GIVE_CARD:
            card_choice = random.choice(turn.player.hand)
            return AIMove(action=Action.GIVE_CARD, card=card_choice)
        elif action_choice is Action.TAKE_CARD:
            return AIMove(action=Action.TAKE_CARD, card=None)
        elif action_choice is Action.PASS_TURN:
            return AIMove(action=Action.PASS_TURN, card=None)
        else:
            raise ValueError("Unknown move by AI")
