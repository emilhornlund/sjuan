# lib/action_decider.py

import random
from typing import List


from .action import Action
from .turn import Turn


class ActionDecider:
    """
    This class is used to decide the next action based on the current state of the game.

    The decision is made by the static method `decide_action` which, in its current implementation, 
    chooses an action randomly from the set of possible actions.
    """

    @staticmethod
    def decide_action(board_matrix: List[List[bool]], turn: Turn) -> Action:
        """
        Decide the next action based on the current state of the board and the possible actions.

        The current implementation randomly selects an action from the set of possible actions.

        :param board_matrix: The current state of the board, represented as a 2D list of boolean values.
        :param turn: The current turn, which contains the set of possible actions.
        :return: The chosen action.
        """

        # Randomly choose an action from the set of possible actions
        return random.choice(list(turn.actions))
