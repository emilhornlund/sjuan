# lib/board.py

from typing import Dict, List, Optional, Type

from .constants import Suit, Rank
from .card import Card


class Board:
    """
    Class representing the game board. Each board has a set of cards organized by suit and rank,
    and methods to add cards to the board, get valid cards, and check if a card is valid.
    """

    def __init__(self) -> None:
        """
        Initializes an empty board for the game.
        """

        self.__board: Dict[Suit, List[Optional[Card]]] = {
            suit: [None] * len(Rank) for suit in Suit}

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the board if it's valid.
        Raises a ValueError if the card is not valid.

        :param card: Card to be added to the board.
        """

        if self.is_valid_card(card):
            self.__board[card.suit][card.rank.value - 1] = card
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

        if self.__has_card(card):
            return False

        if not self.__has_card_by_suit_rank(Suit.HEARTS, Rank.SEVEN):
            return card == Card(Suit.HEARTS, Rank.SEVEN)

        if self.__is_seven_of_any_suit(card) or self.__is_adjacent_to_existing_card(card):
            return True

        return False

    def __is_seven_of_any_suit(self, card: Card) -> bool:
        """
        Checks if a card is a seven of any suit.
        Returns a boolean indicating whether the card is a seven.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is a seven.
        """

        return card.rank == Rank.SEVEN

    def __is_adjacent_to_existing_card(self, card: Card) -> bool:
        """
        Checks if a card is adjacent (in rank) to an existing card on the board in the same suit.
        Returns a boolean indicating whether the card is adjacent to an existing card.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is adjacent to an existing card.
        """

        return self.__has_card_by_suit_rank(card.suit, card.rank.get_rank_below()) or self.__has_card_by_suit_rank(card.suit, card.rank.get_rank_above())

    def __has_card(self, card: Card) -> bool:
        """
        Checks if a card is already on the board.
        Returns a boolean indicating whether the card is on the board.

        :param card: Card to be checked.
        :return: Boolean indicating whether the card is on the board.
        """

        return self.__has_card_by_suit_rank(card.suit, card.rank)

    def __has_card_by_suit_rank(self, suit: Suit, rank: Rank) -> bool:
        """
        Checks if a card of a certain suit and rank is on the board.
        Returns a boolean indicating whether the card is on the board.

        :param suit: Suit of the card to be checked.
        :param rank: Rank of the card to be checked.
        :return: Boolean indicating whether the card is on the board.
        """

        return self.__board[suit][rank.value - 1] is not None
