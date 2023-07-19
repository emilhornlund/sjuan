# lib/card.py

from .constants import Suit, Rank


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        """Initializes a card with a given suit and rank."""
        self.suit = suit
        self.rank = rank

    def __hash__(self):
        """Returns a hash value for a card, which is a combination of its suit and rank."""
        return hash((self.suit, self.rank))

    def __eq__(self, other_card: 'Card'):
        """Checks if two cards are the same (i.e., have the same suit and rank)."""
        return isinstance(other_card, Card) and self.suit == other_card.suit and self.rank == other_card.rank

    def __repr__(self):
        """Returns a string representation of the card."""
        return f"{self.rank.name} of {self.suit.name}"
