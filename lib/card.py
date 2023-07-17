# lib/card.py

from .constants import Suit, Rank


# Define a Card with a Suit and Rank
class Card:
    # Initialize a card with a rank and a suit
    # Args:
    #     rank (Rank): The rank of the card
    #     suit (Suit): The suit of the card
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit  # Suit of the Card (Hearts, Diamonds, Clubs, Spades)
        self.rank = rank  # Rank of the Card (Ace, 2, ..., King)

    # Return a string representation of the card
    # Returns:
    #     str: The string representation of the card
    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name}"
