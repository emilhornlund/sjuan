# tests/test_card.py

from lib.constants import Suit, Rank
from lib.card import Card


def test_card_creation():
    card = Card(Suit.HEARTS, Rank.SEVEN)
    assert card.suit == Suit.HEARTS
    assert card.rank == Rank.SEVEN


def test_card_string_representation():
    card = Card(Suit.HEARTS, Rank.SEVEN)
    assert str(card) == "SEVEN of HEARTS"
