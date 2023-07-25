# tests/test_card.py

import unittest

from lib.card import Card, Suit, Rank


class TestCard(unittest.TestCase):

    def test_card_creation(self) -> None:
        """Test that a Card is properly created with given Suit and Rank."""
        card = Card(Suit.HEARTS, Rank.SEVEN)

        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.SEVEN)

    def test_card_equality(self) -> None:
        """Test that two Cards with same Suit and Rank are considered equal."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.HEARTS, Rank.SEVEN)

        self.assertEqual(card1, card2)

    def test_card_inequality(self) -> None:
        """Test that two Cards with different Suits and Ranks are not equal."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.DIAMONDS, Rank.ACE)

        self.assertNotEqual(card1, card2)

    def test_card_string_representation(self) -> None:
        """Test that string representation of a Card is correct."""
        card = Card(Suit.HEARTS, Rank.SEVEN)
        assert str(card) == "SEVEN of HEARTS"


if __name__ == '__main__':
    unittest.main()
