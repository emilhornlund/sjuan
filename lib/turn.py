# lib/turn.py

from .board import Board
from .card import Card
from .constants import Action, Suit, Rank
from .deck import Deck
from .player import Player


class Turn:
    def __init__(self, actions: list[Action], player: Player, valid_cards: list[Card]):
        self.__actions: list[Action] = actions
        self.__player: Player = player
        self.__valid_cards: list[Card] = valid_cards

    @property
    def actions(self) -> list[Action]:
        return self.__actions

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def valid_cards(self) -> list[Card]:
        return self.__valid_cards
