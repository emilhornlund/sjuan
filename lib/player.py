# lib/player.py

from typing import List

from .constants import Suit, Rank
from .card import Card


class Player:
    def __init__(self, name: str):
        self.__name: str = name
        self.__hand: List[Card] = []

    def get_name(self):
        return self.__name

    def add_card(self, card: Card):
        self.__hand.append(card)

    def remove_card(self, card: Card):
        self.__hand.remove(card)

    def has_card(self, card: Card):
        return card in self.__hand

    def get_card(self, index: int):
        if 0 <= index < len(self.__hand):
            return self.__hand[index]
        else:
            return None

    def get_hand_size(self):
        return len(self.__hand)

    def __repr__(self):
        return f"Player: {self.__name}, Hand: {self.__hand}"
