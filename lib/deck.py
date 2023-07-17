# lib/deck.py

import random
from .constants import Suit, Rank
from .card import Card


# Define a Deck of Cards
class Deck:
    def __init__(self):
        # Generate a standard deck of 52 cards
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal one card from the top of the deck
    # Returns:
    #     Card: The dealt card
    def deal(self):
        return self.cards.pop()

    # Get the number of cards remaining in the deck
    # Returns:
    #     int: The number of cards remaining
    def __len__(self):
        return len(self.cards)

    # Return the string representation of the Deck
    # Returns:
    #     str: The string representation of the deck
    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
