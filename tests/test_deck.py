# tests/test_deck.py

import unittest
from lib.deck import Deck


class TestDeck(unittest.TestCase):
    def setUp(self):
        """Set up a deck object for use in test cases."""
        self.deck = Deck()

    def test_deck_creation_has_52_cards(self):
        """Test that a new deck is properly initialized with 52 cards."""
        self.assertEqual(len(self.deck.cards), 52)

    def test_shuffle_changes_card_order(self):
        """Test that shuffling the deck changes the order of the cards."""
        cards_before_shuffling = list(self.deck.cards)
        self.deck.shuffle()
        self.assertNotEqual(cards_before_shuffling, self.deck.cards)

    def test_deal_reduces_deck_size_by_one(self):
        """Test that dealing a card reduces the size of the deck by 1."""
        self.deck.deal()
        self.assertEqual(len(self.deck.cards), 51)

    def test_string_representation_is_as_expected(self):
        """Test that the string representation of a deck is as expected."""
        self.assertEqual(str(self.deck), "Deck of 52 cards")

    def test_deal_from_empty_deck_raises_error(self):
        """Test that attempting to deal from an empty deck raises a ValueError."""
        # Remove all cards from the deck
        for _ in range(52):
            self.deck.deal()

        self.assertTrue(self.deck.empty())

        with self.assertRaises(ValueError) as context:
            self.deck.deal()

        self.assertEqual(str(context.exception),
                         "Cannot deal from an empty deck.")


if __name__ == '__main__':
    unittest.main()
