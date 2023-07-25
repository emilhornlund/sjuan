# tests/test_board.py

import unittest

from lib.board import Board
from lib.card import Card, Suit, Rank


class TestBoard(unittest.TestCase):

    def test_board_get_valid_cards(self) -> None:
        """Test getting valid cards from the board considering the game progression."""
        board = Board()

        all_cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        valid_cards = board.get_valid_cards(all_cards)

        # At the start of the game, only the seven of hearts should be valid
        self.assertEqual(valid_cards, [Card(Suit.HEARTS, Rank.SEVEN)])

        # Test the game progression by adding cards and checking the valid cards
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:

            # Add the seven of each suit
            board.add_card(Card(suit, Rank.SEVEN))

            # Check the valid cards after adding the seven
            valid_cards = board.get_valid_cards(all_cards)

            # If the suit is hearts, six and eight should be valid, but seven should not be
            # For other suits, seven should not be valid since it's already on the board
            if suit == Suit.HEARTS:
                self.assertIn(Card(suit, Rank.SIX), valid_cards)
                self.assertIn(Card(suit, Rank.EIGHT), valid_cards)
            else:
                self.assertNotIn(Card(suit, Rank.SEVEN), valid_cards)

            # Now test the game progression for each suit, starting from six down to Ace, then from eight up to King
            # In each step, add a card and check the valid cards
            for rank in reversed(list(Rank)[0:6]):  # SIX to ACE
                board.add_card(Card(suit, rank))
                valid_cards = board.get_valid_cards(all_cards)

                # The valid cards should be the next rank down and the eight of the same suit, and the seven of the next suit
                expected_valid_cards = [Card(suit, Rank(
                    rank.value - 1)) if rank.value > Rank.ACE.value else None, Card(suit, Rank.EIGHT)]
                if suit.value < Suit.SPADES.value:
                    expected_valid_cards.append(
                        Card(Suit(suit.value + 1), Rank.SEVEN))
                self.assertTrue(
                    set(filter(None, expected_valid_cards)).issubset(set(valid_cards)))

            # Similarly, test the game progression from eight up to King
            for rank in list(Rank)[7:]:  # EIGHT to KING
                board.add_card(Card(suit, rank))
                valid_cards = board.get_valid_cards(all_cards)

                # The valid cards should be the next rank up and the seven of the next suit
                expected_valid_cards = [
                    Card(suit, Rank(rank.value + 1)) if rank.value < Rank.KING.value else None]
                if suit.value < Suit.SPADES.value:
                    expected_valid_cards.append(
                        Card(Suit(suit.value + 1), Rank.SEVEN))
                self.assertTrue(
                    set(filter(None, expected_valid_cards)).issubset(set(valid_cards)))

        # At the end of the game, no cards should be valid
        valid_cards = board.get_valid_cards(all_cards)
        self.assertEqual(valid_cards, [])

    def test_board_is_valid_card(self) -> None:
        """Test the validation of a card considering the game progression."""
        # This function is used to add a card to the board and test the valid cards
        def add_card_and_test(suit, rank, next_rank) -> None:
            current_card = Card(suit, rank)
            future_card = Card(suit, next_rank)

            # The current card should be valid before adding it to the board
            self.assertTrue(board.is_valid_card(current_card))

            # The future card should not be valid before the current card is added
            if next_rank is not None:
                self.assertFalse(board.is_valid_card(future_card))

            # Add the current card to the board
            board.add_card(current_card)

            # Now the current card should not be valid since it's already on the board
            self.assertFalse(board.is_valid_card(current_card))

            # The future card should now be valid
            if next_rank is not None:
                self.assertTrue(board.is_valid_card(future_card))

        board = Board()

        # Test the game progression for each suit
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:

            # Start with the seven of each suit
            current_card = Card(suit, Rank.SEVEN)
            next_card_lower = Card(suit, Rank.SIX)
            next_card_higher = Card(suit, Rank.EIGHT)

            # Before adding the seven, it should be valid, but six and eight should not be
            self.assertTrue(board.is_valid_card(current_card))
            self.assertFalse(board.is_valid_card(next_card_lower))
            self.assertFalse(board.is_valid_card(next_card_higher))

            # Add the seven to the board
            board.add_card(current_card)

            # Now the seven should not be valid, but six and eight should be
            self.assertFalse(board.is_valid_card(current_card))
            self.assertTrue(board.is_valid_card(next_card_lower))
            self.assertTrue(board.is_valid_card(next_card_higher))

            # Now test the game progression for each suit, starting from six down to Ace, then from eight up to King
            # In each step, add a card and check the valid cards
            for rank in reversed(list(Rank)[0:6]):  # SIX to ACE
                next_rank = Rank(
                    rank.value - 1) if rank.value > Rank.ACE.value else None
                add_card_and_test(suit, rank, next_rank)

            for rank in list(Rank)[7:]:  # EIGHT to KING
                next_rank = Rank(
                    rank.value + 1) if rank.value < Rank.KING.value else None
                add_card_and_test(suit, rank, next_rank)

    def test_add_invalid_card_raises_error(self) -> None:
        """Test that trying to add an invalid card to the board raises an error."""
        board = Board()
        invalid_card = Card(Suit.HEARTS, Rank.SIX)
        with self.assertRaises(ValueError) as context:
            board.add_card(invalid_card)
        self.assertEqual(str(context.exception),
                         f"Invalid card: {invalid_card}")

    def test_cards_are_hashable(self) -> None:
        """Test that cards can be added to a set, which requires them to be hashable."""
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.HEARTS, Rank.SEVEN)
        card_set = {card1, card2}
        self.assertEqual(len(card_set), 1)


if __name__ == '__main__':
    unittest.main()
