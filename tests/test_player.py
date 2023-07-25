# tests/test_player.py

import unittest
from lib.card import Card, Suit, Rank
from lib.player import Player, PlayerType


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a player object and a card object for use in test cases."""
        self.player = Player("Alice", PlayerType.HUMAN)
        self.card = Card(Suit.HEARTS, Rank.SEVEN)

    def test_player_creation_with_name_and_type_and_empty_hand(self) -> None:
        """Test that a player is properly initialized with a name and an empty hand."""
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(self.player.type, PlayerType.HUMAN)
        self.assertEqual(len(self.player.hand), 0)

    def test_add_card_increases_hand_size(self) -> None:
        """Test that adding a card increases the size of the player's hand by 1."""
        self.player.add_card(self.card)
        self.assertEqual(len(self.player.hand), 1)

    def test_hand_is_sorted_after_adding_cards(self) -> None:
        """Test that the player's hand remains sorted after adding cards."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.DIAMONDS, Rank.KING)
        card3 = Card(Suit.HEARTS, Rank.ACE)

        # Add cards in a random order
        self.player.add_card(card1)
        self.player.add_card(card2)
        self.player.add_card(card3)

        # Check that the hand is sorted correctly (first by suit, then by rank)
        self.assertEqual(self.player.hand, [card3, card1, card2])

    def test_remove_card_decreases_hand_size(self) -> None:
        """Test that removing a card decreases the size of the player's hand by 1."""
        self.player.add_card(self.card)
        self.player.remove_card(self.card)
        self.assertEqual(len(self.player.hand), 0)

    def test_has_card_returns_correct_boolean(self) -> None:
        """Test that has_card method returns true if the card is in the hand, false otherwise."""
        self.player.add_card(self.card)
        self.assertTrue(self.player.has_card(self.card))
        self.player.remove_card(self.card)
        self.assertFalse(self.player.has_card(self.card))

    def test_players_with_same_name_are_equal(self) -> None:
        """Test that two players with the same name and hand are considered equal."""
        player2 = Player("Alice", PlayerType.HUMAN)
        player2.add_card(Card(Suit.HEARTS, Rank.SEVEN))
        self.assertEqual(self.player, player2)

    def test_players_with_different_name_or_hand_are_not_equal(self) -> None:
        """Test that two players with different names or hands are not considered equal."""
        player2 = Player("Bob", PlayerType.HUMAN)
        player2.add_card(Card(Suit.DIAMONDS, Rank.ACE))
        self.assertNotEqual(self.player, player2)

    def test_string_representation_with_empty_hand(self) -> None:
        """Test that the string representation of a player with an empty hand is as expected."""
        self.assertEqual(str(self.player),
                         "Player: Alice, Type: Human, Hand: []")

    def test_string_representation_with_cards_in_hand(self) -> None:
        """Test that the string representation of a player with cards in their hand is as expected."""
        self.player.add_card(self.card)
        self.assertEqual(str(self.player),
                         f"Player: Alice, Type: Human, Hand: [{self.card}]")


if __name__ == '__main__':
    unittest.main()
