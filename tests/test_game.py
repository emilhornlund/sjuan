# tests/test_game.py

import unittest
import random
from lib.action import Action, ActionType

from lib.card import Card, Suit, Rank
from lib.game import Game, PlayerInfo
from lib.player import PlayerType


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a game object for use in test cases."""

        self.game = Game(player_infos=[
            PlayerInfo(name="Bob", type=PlayerType.HUMAN),
            PlayerInfo(name="Alice", type=PlayerType.HUMAN),
            PlayerInfo(name="Ted", type=PlayerType.HUMAN),
            PlayerInfo(name="Eve", type=PlayerType.HUMAN)])

    def test_game_initialization(self) -> None:
        """Test that a new game is correctly initialized."""

        self.assert_game_reset()

    def test_game_start(self) -> None:
        """Test that a game correctly starts."""

        self.game.start()

        # Check that the deck is empty and each player has 13 cards
        self.assertTrue(self.game._Game__deck.empty)
        for player in self.game._Game__players:
            self.assertEqual(len(player.hand), 13)

    def test_game_reset(self) -> None:
        """Test that a game can be correctly reset."""

        self.game.start()
        self.assertTrue(self.game._Game__deck.empty)
        self.game.reset()
        self.assert_game_reset()

    def test_game_first_turn(self) -> None:
        """Test that the first turn of a game is correctly set up."""

        self.game.start()

        # Check that the correct player starts, has the right actions and valid cards
        self.assertTrue(self.game.turn.player.name in [
                        "Bob", "Alice", "Ted", "Eve"])
        self.assertEqual(len(self.game.turn.player.hand), 13)
        self.assertEqual(len(self.game.turn.actions), 1)
        self.assertEqual(self.game.turn.actions, set(
            [Action(type=ActionType.PLAY_CARD, card=Card(Suit.HEARTS, Rank.SEVEN))]))

    def assert_game_reset(self) -> None:
        """Check that a game is correctly reset."""

        self.assertEqual(len(self.game._Game__players), 4)

        # Check that each player has no cards in hand after reset
        for player in self.game._Game__players:
            self.assertEqual(len(player.hand), 0)

    def test_game_full_round(self) -> None:
        """Test that a full round of a game is correctly played."""

        self.game.start()

        # Simulate a full round of game
        while not self.game.is_finished():
            action_choice = random.choice(list(self.game.turn.actions))
            self.game.execute_action(action=action_choice)

        # Check that all players have no cards left.
        for player in self.game._Game__players:
            self.assertEqual(len(player.hand), 0)

        # Check that all players are in the finished_players list
        finished_player_names = [
            player.name for player in self.game.finished_players]
        self.assertEqual(len(self.game.finished_players), 4)
        self.assertIn("Bob", finished_player_names)
        self.assertIn("Alice", finished_player_names)
        self.assertIn("Ted", finished_player_names)
        self.assertIn("Eve", finished_player_names)

    def test_invalid_play_card(self) -> None:
        """Test that playing an invalid card raises an error."""

        self.game.start()

        # This card is not in the valid cards
        invalid_card = Card(Suit.HEARTS, Rank.ACE)
        with self.assertRaises(ValueError) as context:
            self.game.execute_action(
                Action(type=ActionType.PLAY_CARD, card=invalid_card))
        self.assertEqual(str(context.exception),
                         f"Invalid action Play ACE of HEARTS")

    def test_take_card_when_not_allowed(self) -> None:
        """Test that taking a card when not allowed raises an error."""

        self.game.start()
        with self.assertRaises(ValueError) as context:
            # Can't take card on first turn
            self.game.execute_action(Action(type=ActionType.TAKE_CARD))
        self.assertEqual(str(context.exception),
                         f"Invalid action Take card")

    def test_give_card_when_not_allowed(self) -> None:
        """Test that giving a card when not allowed raises an error."""

        self.game.start()
        card_to_give = Card(suit=Suit.HEARTS, rank=Rank.SEVEN)
        with self.assertRaises(ValueError) as context:
            # Can't give card on first turn
            self.game.execute_action(
                Action(type=ActionType.GIVE_CARD, card=card_to_give))
        self.assertEqual(str(context.exception),
                         f"Invalid action Give SEVEN of HEARTS")

    def test_pass_turn_when_not_allowed(self) -> None:
        """Test that passing a turn when not allowed raises an error."""

        self.game.start()
        with self.assertRaises(ValueError) as context:
            # Can't pass turn on first turn
            self.game.execute_action(Action(type=ActionType.PASS_TURN))
        self.assertEqual(str(context.exception),
                         f"Invalid action Pass turn")


if __name__ == '__main__':
    unittest.main()
