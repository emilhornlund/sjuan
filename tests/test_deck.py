# tests/test_deck.py

from lib.deck import Deck


def test_deck_creation():
    deck = Deck()
    assert len(deck) == 52


def test_deck_shuffling():
    deck = Deck()
    cards_before_shuffling = list(deck.cards)
    deck.shuffle()
    assert list(deck.cards) != cards_before_shuffling


def test_deck_dealing():
    deck = Deck()
    card = deck.deal()
    assert len(deck) == 51


def test_deck_string_representation():
    deck = Deck()
    assert str(deck) == "Deck of 52 cards"
