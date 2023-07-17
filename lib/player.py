# lib/player.py

from .card import Card


# Define a Player in the Card Game
class Player:
    # Initialize a player with a name and an empty hand
    # Args:
    #     name (str): The name of the player
    def __init__(self, name):
        self.name = name
        self.hand = []

    # Add a card to the player's hand
    # Args:
    #     card (Card): The card to add to the hand
    def add_card(self, card):
        self.hand.append(card)

    # Remove a card from the player's hand.
    # Args:
    #     card (Card): The card to remove from the hand
    def remove_card(self, card):
        self.hand.remove(card)

    # Check if the player has a specific card in their hand
    # Args:
    #     card (Card): The card to check
    # Returns:
    #     bool: True if the player has the card, False otherwise
    def has_card(self, card):
        return card in self.hand

    # Get the number of cards in the player's hand
    # Returns:
    #     int: The number of cards in the hand
    def __len__(self):
        return len(self.hand)

    # Return a string representation of the player
    # Returns:
    #     str: The string representation of the player
    def __repr__(self):
        return f"Player: {self.name}, Hand: {self.hand}"
