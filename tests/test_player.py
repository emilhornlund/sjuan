# tests/test_player.py

from lib.player import Player
from lib.card import Card


def test_player_creation():
    player = Player("Alice")
    assert player.name == "Alice"
    assert player.hand == []


def test_add_card():
    player = Player("Alice")
    card = Card("Hearts", "7")
    player.add_card(card)
    assert card in player.hand
    assert len(player) == 1


def test_remove_card():
    player = Player("Alice")
    card = Card("Hearts", "7")
    player.add_card(card)
    player.remove_card(card)
    assert card not in player.hand
    assert len(player) == 0


def test_has_card():
    player = Player("Alice")
    card = Card("Hearts", "7")
    player.add_card(card)
    assert player.has_card(card)
    assert len(player) == 1


def test_player_string_representation():
    player = Player("Alice")
    assert str(player) == "Player: Alice, Hand: []"
