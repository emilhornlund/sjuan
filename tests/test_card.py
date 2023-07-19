# tests/test_card.py

import unittest

from lib.constants import Suit, Rank
from lib.card import Card


class TestCard(unittest.TestCase):

    def test_card_creation(self):
        """Test that a Card is properly created with given Suit and Rank."""
        card = Card(Suit.HEARTS, Rank.SEVEN)

        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.SEVEN)

    def test_card_equality(self):
        """Test that two Cards with same Suit and Rank are considered equal."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.HEARTS, Rank.SEVEN)

        self.assertEqual(card1, card2)

    def test_card_inequality(self):
        """Test that two Cards with different Suits and Ranks are not equal."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.DIAMONDS, Rank.ACE)

        self.assertNotEqual(card1, card2)

    def test_card_string_representation(self):
        """Test that string representation of a Card is correct."""
        card = Card(Suit.HEARTS, Rank.SEVEN)
        assert str(card) == "SEVEN of HEARTS"


if __name__ == '__main__':
    unittest.main()
