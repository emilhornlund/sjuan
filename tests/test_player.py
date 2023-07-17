# tests/test_player.py

import unittest

from lib.constants import Suit, Rank
from lib.player import Player
from lib.card import Card


class TestPlayer(unittest.TestCase):

    def test_player_creation(self):
        player = Player("Alice")

        self.assertEqual(player.get_name(), "Alice")
        self.assertEqual(player.get_hand_size(), 0)

    def test_player_add_card(self):
        player = Player("Alice")
        card = Card(Suit.HEARTS, Rank.SEVEN)

        player.add_card(card)

        self.assertTrue(player.has_card(card))
        self.assertEqual(player.get_hand_size(), 1)
        self.assertEqual(player.get_card(0), card)

    def test_player_remove_card(self):
        player = Player("Alice")
        card = Card(Suit.HEARTS, Rank.SEVEN)

        player.add_card(card)

        self.assertTrue(player.has_card(card))
        self.assertEqual(player.get_hand_size(), 1)
        self.assertEqual(player.get_card(0), card)

        player.remove_card(card)

        self.assertFalse(player.has_card(card))
        self.assertEqual(player.get_hand_size(), 0)

    def test_player_string_representation(self):
        player = Player("Alice")

        self.assertEqual(str(player), "Player: Alice, Hand: []")


if __name__ == '__main__':
    unittest.main()
