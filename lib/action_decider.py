# lib/action_decider.py

from typing import Dict, List, Tuple

from .action import Action, ActionType
from .card import Card, Rank, Suit
from .turn import Turn


class ActionDecider:
    """
    The ActionDecider class is responsible for deciding the best action to take based on the state of the game board and 
    the available actions for the current turn.
    """

    @staticmethod
    def decide_action(board_matrix: List[List[bool]], turn: Turn) -> Action:
        """
        Decide the best action to take given the state of the game board and the available actions for the current turn.

        :param board_matrix: A 2D list where each sublist corresponds to a suit and each boolean in the sublist 
                             indicates whether the card of that suit and rank has been played (True if it has, False otherwise).
        :param turn: The current turn, which includes the available actions.
        :return: The best action to take.
        """

        # Define the priority for each action type
        action_priorities = {
            ActionType.PLAY_ALL_CARDS: 1,
            ActionType.GIVE_CARD: 2,
            ActionType.PLAY_CARD: 3,
            ActionType.TAKE_CARD: 4,
            ActionType.PASS_TURN: 5
        }

        # Group actions by their type
        actions_by_type = {action_type: [] for action_type in ActionType}
        for action in turn.actions:
            actions_by_type[action.type].append(action)

        # Iterate over action types in order of their priority
        for action_type in sorted(action_priorities, key=action_priorities.get):
            if action_type == ActionType.PLAY_CARD:
                # Analyze the board and score the cards for this action type
                board_state = ActionDecider._ActionDecider__analyze_board(
                    board_matrix)
                scores = ActionDecider._ActionDecider__score_cards(
                    [action.card for action in actions_by_type[action_type]], board_state)
                if scores:
                    # Choose the card with the lowest score (i.e., the best card to play)
                    card_choice = min(scores, key=scores.get)
                    # Return the action that corresponds to the chosen card
                    return [action for action in actions_by_type[action_type] if action.card == card_choice][0]
            elif action_type == ActionType.GIVE_CARD:
                # Analyze the board and score the cards for this action type
                board_state = ActionDecider._ActionDecider__analyze_board(
                    board_matrix)
                scores = ActionDecider._ActionDecider__score_cards(
                    [action.card for action in actions_by_type[action_type]], board_state)
                if scores:
                    # Choose the card with the highest score (i.e., the best card to give)
                    card_choice = max(scores, key=scores.get)
                    # Return the action that corresponds to the chosen card
                    return [action for action in actions_by_type[action_type] if action.card == card_choice][0]
            elif actions_by_type[action_type]:
                # If there are any actions of this type, return the first one
                return actions_by_type[action_type][0]

        # If no decision could be made, raise an exception
        raise ValueError("No valid actions available for the current turn.")

    @staticmethod
    def __analyze_board(board_matrix: List[List[bool]]) -> Dict[Suit, Tuple[Rank, Rank]]:
        """
        Analyze the game board and determine the minimum and maximum card rank for each suit.

        :param board_matrix: A 2D list where each sublist corresponds to a suit and each boolean in the sublist 
                                indicates whether the card of that suit and rank has been played.
        :return: A dictionary mapping each suit to a tuple of the minimum and maximum card rank for that suit.
        """

        board_state = {}
        for suit, suit_cards in enumerate(board_matrix):
            played_cards = [Rank(rank+1)
                            for rank, played in enumerate(suit_cards) if played]
            if played_cards:
                min_card = min(played_cards)
                max_card = max(played_cards)
            else:
                # If no cards of this suit have been played, assume the minimum and maximum card rank are both SEVEN
                min_card = max_card = Rank.SEVEN
            board_state[Suit(suit+1)] = (min_card, max_card)
        return board_state

    @staticmethod
    def __score_cards(cards: List[Card], board_state: Dict[Suit, Tuple[Rank, Rank]]) -> Dict[Card, int]:
        """
        Score each card based on the current state of the game board. A lower score indicates a better card to play.
        The score is calculated based on the difference between the rank of the card and the nearest rank that can be played on the board.

        :param cards: A list of cards to score.
        :param board_state: A dictionary mapping each suit to a tuple of the minimum and maximum card rank for that suit.
        :return: A dictionary mapping each card to its score.
        """

        scores = {}
        for card in cards:
            min_card, max_card = board_state[card.suit]
            if card.rank > max_card:
                score = card.rank.value - max_card.value
            elif card.rank < min_card:
                score = min_card.value - card.rank.value
            else:
                # If the card can be played immediately, its score is 0
                score = 0
            scores[card] = score
        return scores
