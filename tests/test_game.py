# tests/test_game.py

import unittest
from lib.card import Card
from lib.constants import Action, Suit, Rank
from lib.game import Game, GameMode


class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up a game object for use in test cases."""

        self.game = Game(GameMode.PARTY, ["Bob", "Alice", "Ted", "Eve"])

    def test_game_initialization(self):
        """Test that a new game is correctly initialized."""

        self.assert_game_reset()

    def test_game_start(self):
        """Test that a game correctly starts."""

        self.game.start()

        # Check that the deck is empty and each player has 13 cards
        self.assertTrue(self.game._Game__deck.empty)
        for player in self.game._Game__players:
            self.assertEqual(len(player.hand), 13)

    def test_game_reset(self):
        """Test that a game can be correctly reset."""

        self.game.start()
        self.assertTrue(self.game._Game__deck.empty)
        self.game.reset()
        self.assert_game_reset()

    def test_game_first_turn(self):
        """Test that the first turn of a game is correctly set up."""

        self.game.start()

        # Check that the correct player starts, has the right actions and valid cards
        self.assertTrue(self.game.turn.player.name in [
                        "Bob", "Alice", "Ted", "Eve"])
        self.assertEqual(len(self.game.turn.player.hand), 13)
        self.assertEqual(self.game.turn.actions, [Action.PLAY_CARD])
        self.assertEqual(self.game.turn.valid_cards, [
                         Card(Suit.HEARTS, Rank.SEVEN)])

    def assert_game_reset(self):
        """Check that a game is correctly reset."""

        self.assertEqual(len(self.game._Game__players), 4)

        # Check that each player has no cards in hand after reset
        for player in self.game._Game__players:
            self.assertEqual(len(player.hand), 0)

    def test_game_full_round(self):
        """Test that a full round of a game is correctly played."""

        self.game.start()

        # Simulate a full round of game
        while not self.game.is_finished():
            if Action.PLAY_CARD in self.game.turn.actions:
                card_to_play = self.game.turn.valid_cards[0]
                self.game.play_card(card_to_play)
            elif Action.GIVE_CARD in self.game.turn.actions:
                card_to_give = self.game.turn.valid_cards[0]
                self.game.give_card(card_to_give)
            elif Action.TAKE_CARD in self.game.turn.actions:
                self.game.take_card()
            elif Action.PASS_TURN in self.game.turn.actions:
                self.game.pass_turn()

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

    def test_invalid_play_card(self):
        """Test that playing an invalid card raises an error."""

        self.game.start()

        # This card is not in the valid cards
        invalid_card = Card(Suit.HEARTS, Rank.ACE)
        with self.assertRaises(ValueError) as context:
            self.game.play_card(invalid_card)
        self.assertEqual(str(context.exception),
                         f"Invalid card: {invalid_card}")

    def test_take_card_when_not_allowed(self):
        """Test that taking a card when not allowed raises an error."""

        self.game.start()
        with self.assertRaises(ValueError) as context:
            self.game.take_card()  # Can't take card on first turn
        self.assertEqual(str(context.exception),
                         f"Invalid action in {[Action.PLAY_CARD]}")

    def test_give_card_when_not_allowed(self):
        """Test that giving a card when not allowed raises an error."""

        self.game.start()
        card_to_give = self.game.turn.valid_cards[0]
        with self.assertRaises(ValueError) as context:
            self.game.give_card(card_to_give)  # Can't give card on first turn
        self.assertEqual(str(context.exception),
                         f"Invalid action in {[Action.PLAY_CARD]}")

    def test_pass_turn_when_not_allowed(self):
        """Test that passing a turn when not allowed raises an error."""

        self.game.start()
        with self.assertRaises(ValueError) as context:
            self.game.pass_turn()  # Can't pass turn on first turn
        self.assertEqual(str(context.exception),
                         f"Invalid action in {[Action.PLAY_CARD]}")


if __name__ == '__main__':
    unittest.main()
