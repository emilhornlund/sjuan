import unittest
from lib.action import Action, ActionType

from lib.action_decider import ActionDecider
from lib.card import Card, Rank, Suit
from lib.player import Player, PlayerType
from lib.turn import Turn


class TestActionDecider(unittest.TestCase):
    def test_decide_action_play_all_cards(self):
        # Create a board state where no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]

        # Create actions for the turn
        actions = {Action(ActionType.PLAY_ALL_CARDS)}

        # Create a turn with the actions
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # The expected action is to play all cards, because it's the only action available
        expected_action = Action(ActionType.PLAY_ALL_CARDS)

        # Call decide_action and check that it returns the expected action
        actual_action = ActionDecider.decide_action(
            board_matrix=board_matrix, turn=turn)
        self.assertEqual(actual_action, expected_action)

    def test_decide_action_give_card(self):
        # Create a board state where no cards have been played yet
        board_matrix = [
            [False, False, False, False, False, False, True, False,
                False, False, False, False, False],  # Hearts
            [False]*13,  # Diamonds
            [False]*13,  # Clubs
            [False]*13,  # Spades
        ]

        # Create actions for the turn
        actions = {Action(ActionType.GIVE_CARD, Card(Suit.HEARTS, Rank.ACE)), Action(
            ActionType.GIVE_CARD, Card(Suit.HEARTS, Rank.FIVE))}

        # Create a turn with the actions
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # The expected action is to give a card, because it's the only action available
        expected_action = Action(ActionType.GIVE_CARD,
                                 Card(Suit.HEARTS, Rank.ACE))

        # Call decide_action and check that it returns the expected action
        actual_action = ActionDecider.decide_action(board_matrix, turn)
        self.assertEqual(actual_action, expected_action)

    def test_decide_action_play_card(self):
        # Create a board state where no cards have been played yet
        # board_matrix = [[False]*13 for _ in range(4)]

        board_matrix = [
            [False, False, False, False, False, False, True, False,
                False, False, False, False, False],  # Hearts
            [False]*13,  # Diamonds
            [False]*13,  # Clubs
            [False]*13,  # Spades
        ]

        # Create actions for the turn
        actions = {Action(ActionType.PLAY_CARD, Card(Suit.HEARTS, Rank.ACE)), Action(
            ActionType.PLAY_CARD, Card(Suit.HEARTS, Rank.SIX))}

        # Create a turn with the actions
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # The expected action is to play a card, because it's the only action available
        expected_action = Action(ActionType.PLAY_CARD,
                                 Card(Suit.HEARTS, Rank.SIX))

        # Call decide_action and check that it returns the expected action
        actual_action = ActionDecider.decide_action(board_matrix, turn)
        self.assertEqual(actual_action, expected_action)

    def test_decide_action_take_card(self):
        # Create a board state where no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]

        # Create actions for the turn
        actions = {Action(ActionType.TAKE_CARD)}

        # Create a turn with the actions
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # The expected action is to take a card, because it's the only action available
        expected_action = Action(ActionType.TAKE_CARD)

        # Call decide_action and check that it returns the expected action
        actual_action = ActionDecider.decide_action(board_matrix, turn)
        self.assertEqual(actual_action, expected_action)

    def test_decide_action_pass_turn(self):
        # Create a board state where no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]

        # Create actions for the turn
        actions = {Action(ActionType.PASS_TURN)}

        # Create a turn with the actions
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # The expected action is to pass the turn, because it's the only action available
        expected_action = Action(ActionType.PASS_TURN)

        # Call decide_action and check that it returns the expected action
        actual_action = ActionDecider.decide_action(board_matrix, turn)
        self.assertEqual(actual_action, expected_action)

    def test_decide_action_when_multiple_actions_are_possible(self):
        """
        In this test case, all action types are possible, so we check that the decide_action function correctly 
        prioritizes actions according to the predefined priority order.
        """

        # Create a board state where no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]

        # Define the priority for each action type
        action_priorities = {
            ActionType.PLAY_ALL_CARDS: 1,
            ActionType.GIVE_CARD: 2,
            ActionType.PLAY_CARD: 3,
            ActionType.TAKE_CARD: 4,
            ActionType.PASS_TURN: 5
        }

        # Create a turn with all actions
        actions = {
            Action(action_type) if action_type != ActionType.PLAY_CARD and action_type != ActionType.GIVE_CARD
            else Action(action_type, Card(Suit.HEARTS, Rank.ACE))
            for action_type in ActionType
        }
        turn = Turn(actions=actions, player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # Test each priority
        for priority in range(1, 6):
            expected_action_type = [action_type for action_type, action_priority in action_priorities.items(
            ) if action_priority == priority][0]
            expected_action = Action(expected_action_type) if expected_action_type != ActionType.PLAY_CARD and expected_action_type != ActionType.GIVE_CARD else Action(
                expected_action_type, Card(Suit.HEARTS, Rank.ACE))

            # Call decide_action and check that it returns the expected action
            actual_action = ActionDecider.decide_action(board_matrix, turn)
            self.assertEqual(actual_action, expected_action)

            # Remove the action from the turn actions to check the next priority
            turn.actions.remove(expected_action)

    def test_decide_action_no_actions(self):
        # Create a board state where no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]

        # Create a turn with no actions
        turn = Turn(actions=set(), player=Player(
            name="Alice", type=PlayerType.AI), opponents=[])

        # Call decide_action and check that it raises a ValueError
        with self.assertRaises(ValueError):
            ActionDecider.decide_action(board_matrix, turn)

    def test_analyze_board(self):
        board_matrix = [
            [False, False, False, False, False, False, True, False,
                False, False, False, False, False],  # Hearts
            [False, False, False, False, False, True, True, True,
                False, False, False, False, False],  # Diamonds
            [False, False, False, False, False, False, False,
                False, False, False, False, False, False],  # Clubs
            [False, False, False, False, False, False, True,
                True, True, False, False, False, False],  # Spades
        ]
        expected_board_state = {
            Suit.HEARTS: (Rank.SEVEN, Rank.SEVEN),
            Suit.DIAMONDS: (Rank.SIX, Rank.EIGHT),
            Suit.CLUBS: (Rank.SEVEN, Rank.SEVEN),
            Suit.SPADES: (Rank.SEVEN, Rank.NINE),
        }
        actual_board_state = ActionDecider._ActionDecider__analyze_board(
            board_matrix)

        self.assertEqual(actual_board_state, expected_board_state)

    def test_analyze_board_no_cards_played(self):
        # Test when no cards have been played yet
        board_matrix = [[False]*13 for _ in range(4)]
        expected_board_state = {
            Suit.HEARTS: (Rank.SEVEN, Rank.SEVEN),
            Suit.DIAMONDS: (Rank.SEVEN, Rank.SEVEN),
            Suit.CLUBS: (Rank.SEVEN, Rank.SEVEN),
            Suit.SPADES: (Rank.SEVEN, Rank.SEVEN),
        }
        actual_board_state = ActionDecider._ActionDecider__analyze_board(
            board_matrix)
        self.assertEqual(actual_board_state, expected_board_state)

    def test_analyze_board_all_cards_played(self):
        # Test when all cards have been played
        board_matrix = [[True]*13 for _ in range(4)]
        expected_board_state = {
            Suit.HEARTS: (Rank.ACE, Rank.KING),
            Suit.DIAMONDS: (Rank.ACE, Rank.KING),
            Suit.CLUBS: (Rank.ACE, Rank.KING),
            Suit.SPADES: (Rank.ACE, Rank.KING),
        }
        actual_board_state = ActionDecider._ActionDecider__analyze_board(
            board_matrix)
        self.assertEqual(actual_board_state, expected_board_state)

    def test_score_cards(self):
        board_state = {
            Suit.HEARTS: (Rank.SEVEN, Rank.SEVEN),
            Suit.DIAMONDS: (Rank.SIX, Rank.EIGHT),
            Suit.CLUBS: (Rank.SEVEN, Rank.SEVEN),
            Suit.SPADES: (Rank.SEVEN, Rank.NINE),
        }
        cards = [
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.SPADES, Rank.TEN),
        ]
        expected_scores = {
            cards[0]: 1,
            cards[1]: 1,
            cards[2]: 1,
            cards[3]: 1,
        }
        actual_scores = ActionDecider._ActionDecider__score_cards(
            cards, board_state)
        self.assertEqual(actual_scores, expected_scores)

    def test_score_cards_all_playable(self):
        # Test when all cards are playable
        board_state = {
            Suit.HEARTS: (Rank.SIX, Rank.EIGHT),
            Suit.DIAMONDS: (Rank.SIX, Rank.EIGHT),
            Suit.CLUBS: (Rank.SIX, Rank.EIGHT),
            Suit.SPADES: (Rank.SIX, Rank.EIGHT),
        }
        cards = [
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SEVEN),
        ]
        expected_scores = {card: 0 for card in cards}  # All cards are playable
        actual_scores = ActionDecider._ActionDecider__score_cards(
            cards, board_state)
        self.assertEqual(actual_scores, expected_scores)

    def test_score_cards_all_unplayable(self):
        # Test when no cards are playable
        board_state = {
            Suit.HEARTS: (Rank.SEVEN, Rank.SEVEN),
            Suit.DIAMONDS: (Rank.SEVEN, Rank.SEVEN),
            Suit.CLUBS: (Rank.SEVEN, Rank.SEVEN),
            Suit.SPADES: (Rank.SEVEN, Rank.SEVEN),
        }
        cards = [
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.SPADES, Rank.EIGHT),
        ]
        # All cards are one step away from being playable
        expected_scores = {card: 1 for card in cards}
        actual_scores = ActionDecider._ActionDecider__score_cards(
            cards, board_state)
        self.assertEqual(actual_scores, expected_scores)

    def test_score_cards_all_extreme(self):
        # Test when all cards are at their furthest possible position from being playable
        board_state = {
            Suit.HEARTS: (Rank.SEVEN, Rank.SEVEN),
            Suit.DIAMONDS: (Rank.SEVEN, Rank.SEVEN),
            Suit.CLUBS: (Rank.SEVEN, Rank.SEVEN),
            Suit.SPADES: (Rank.SEVEN, Rank.SEVEN),
        }
        cards = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
        ]
        # All cards are six steps away from being playable
        expected_scores = {card: 6 for card in cards}
        actual_scores = ActionDecider._ActionDecider__score_cards(
            cards, board_state)
        self.assertEqual(actual_scores, expected_scores)


if __name__ == '__main__':
    unittest.main()
