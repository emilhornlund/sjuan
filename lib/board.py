# lib/board.py

from .constants import Suit, Rank
from .card import Card


class Board:
    """Represents the game board."""

    def __init__(self):
        """Initializes an empty board for the game."""
        self.__board = {suit: [None] * len(Rank) for suit in Suit}

    def add_card(self, card: Card):
        """
        Adds a card to the board if it's valid.
        Raises a ValueError if the card is not valid.
        """
        if self.is_valid_card(card):
            self.__board[card.suit][card.rank.value - 1] = card
        else:
            raise ValueError(f"Invalid card: {card}")

    def get_valid_cards(self, cards: list[Card]):
        """
        Filters out invalid cards from a given list.
        Returns a list of valid cards.
        """
        return list(filter(self.is_valid_card, cards))

    def is_valid_card(self, card: Card):
        """
        Checks if a card can be played according to the game rules.
        Returns a boolean indicating whether the card is valid.
        """
        if self.__has_card(card):
            return False

        if not self.__has_card_by_suit_rank(Suit.HEARTS, Rank.SEVEN):
            return card == Card(Suit.HEARTS, Rank.SEVEN)

        if self.__is_seven_of_any_suit(card) or self.__is_adjacent_to_existing_card(card):
            return True

        return False

    def __is_seven_of_any_suit(self, card: Card):
        """
        Checks if a card is a seven of any suit.
        Returns a boolean indicating whether the card is a seven.
        """
        return card.rank == Rank.SEVEN

    def __is_adjacent_to_existing_card(self, card: Card):
        """
        Checks if a card is adjacent (in rank) to an existing card on the board in the same suit.
        Returns a boolean indicating whether the card is adjacent to an existing card.
        """
        return self.__has_card_by_suit_rank(card.suit, card.rank.get_rank_bellow()) or self.__has_card_by_suit_rank(card.suit, card.rank.get_rank_above())

    def __has_card(self, card: Card):
        """
        Checks if a card is already on the board.
        Returns a boolean indicating whether the card is on the board.
        """
        return self.__has_card_by_suit_rank(card.suit, card.rank)

    def __has_card_by_suit_rank(self, suit: Suit, rank: Rank):
        """
        Checks if a card of a certain suit and rank is on the board.
        Returns a boolean indicating whether the card is on the board.
        """
        return self.__board[suit][rank.value - 1] is not None
