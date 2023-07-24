# lib/board.py

import copy
from typing import List

from .constants import Suit, Rank
from .card import Card


class Board:
    """
    Class representing the game board in a card game. Each board has a set of cards organized by suit and rank.
    The cards on the board are represented as a matrix of booleans where each cell corresponds to a card identified by its suit and rank.
    The value in a cell is True if the corresponding card is on the board, False otherwise.

    The board provides methods to add cards to the board, get valid cards, and check if a card is valid.
    It also provides a property to access a copy of the internal matrix representing the game board.
    """

    def __init__(self) -> None:
        """
        Initializes an empty board for the game. The board is represented as a matrix of booleans
        where each cell corresponds to a card identified by its suit and rank.
        The value in a cell is True if the corresponding card is on the board, False otherwise.
        """

        self.__matrix: list[list[bool]] = [[False for _ in range(
            len(Rank))] for _ in range(len(Suit))]

    @property
    def matrix(self) -> list[list[bool]]:
        """
        Provides a deep copy of the internal matrix representing the game board.

        Each cell in the returned matrix corresponds to a card identified by its suit and rank.
        The value in a cell is True if the corresponding card is on the board, and False otherwise.
        This allows for safe interaction with the board state without modifying the original data.

        :return: A deep copy of the board's internal matrix.
        """

        return copy.deepcopy(self.__matrix)

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the board if it's valid.
        Raises a ValueError if the card is not valid.

        :param card: Card to be added to the board.
        """

        if not (0 <= card.suit.value - 1 < len(Suit) and 0 <= card.rank.value - 1 < len(Rank)):
            raise ValueError(f"Invalid card: {card}")
        if self.is_valid_card(card):
            self.__matrix[card.suit.value - 1][card.rank.value - 1] = True
        else:
            raise ValueError(f"Invalid card: {card}")

    def get_valid_cards(self, cards: List[Card]) -> List[Card]:
        """
        Filters out invalid cards from a given list.
        Returns a list of valid cards.

        :param cards: List of cards to be filtered.
        :return: List of valid cards.
        """

        return list(filter(self.is_valid_card, cards))

    def is_valid_card(self, card: Card) -> bool:
        """
        Checks if a card can be played according to the game rules.
        Returns a boolean indicating whether the card is valid.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is valid.
        """

        if self.__is_card_on_board(card):
            return False

        if not self.__is_card_on_board_by_suit_rank(Suit.HEARTS, Rank.SEVEN):
            return card == Card(Suit.HEARTS, Rank.SEVEN)

        if self.__is_card_seven_of_any_suit(card) or self.__is_card_adjacent_to_existing_card(card):
            return True

        return False

    def __is_card_seven_of_any_suit(self, card: Card) -> bool:
        """
        Checks if a card is a seven of any suit.
        Returns a boolean indicating whether the card is a seven.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is a seven.
        """

        return card.rank == Rank.SEVEN

    def __is_card_adjacent_to_existing_card(self, card: Card) -> bool:
        """
        Checks if a card is adjacent (in rank) to an existing card on the board in the same suit.
        Returns a boolean indicating whether the card is adjacent to an existing card.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is adjacent to an existing card.
        """

        return self.__is_card_on_board_by_suit_rank(card.suit, card.rank.get_rank_below()) or self.__is_card_on_board_by_suit_rank(card.suit, card.rank.get_rank_above())

    def __is_card_on_board(self, card: Card) -> bool:
        """
        Checks if a card is already on the board.
        Returns a boolean indicating whether the card is on the board.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is on the board.
        """

        return self.__is_card_on_board_by_suit_rank(card.suit, card.rank)

    def __is_card_on_board_by_suit_rank(self, suit: Suit, rank: Rank) -> bool:
        """
        Checks if a card of a certain suit and rank is already on the board.
        Returns a boolean indicating whether the card is on the board.

        :param suit: Suit of the card to be checked.
        :param rank: Rank of the card to be checked.
        :return: Boolean indicating whether the card is on the board.
        """

        if not (0 <= suit.value - 1 < len(Suit) and 0 <= rank.value - 1 < len(Rank)):
            raise ValueError(
                f"Invalid card for suit: {suit.value} or rank: {rank.value}")

        return self.__matrix[suit.value - 1][rank.value - 1] is True
