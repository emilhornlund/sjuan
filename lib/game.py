# lib/game.py

from typing import List, NamedTuple

from .board import Board
from .card import Card
from .constants import Action, Suit, Rank
from .deck import Deck
from .player import Player, PlayerType
from .turn import Turn


class PlayerInfo(NamedTuple):
    name: str
    type: PlayerType


class Game:
    """
    Class representing the "Sjuan" card game with given rules and player actions.
    """

    def __init__(self, player_infos: List[PlayerInfo]) -> None:
        """
        Constructor for the Game class.

        :param player_names: List of player names.
        """

        self.__player_infos: List[PlayerInfo] = player_infos
        self.__finished_players: List[Player] = []
        self.reset()

    def reset(self) -> None:
        """
        Reset the game, initialize players, deck, board and current turn.
        """

        self.__players: List[Player] = [
            Player(player_info.name, player_info.type) for player_info in self.__player_infos]
        self.__finished_players.clear()
        self.__current_player_index: int = 0
        self.__deck: Deck = Deck()
        self.__board: Board = Board()
        self.__current_turn: Turn = None

    def start(self) -> None:
        """
        Start the game by shuffling the deck, dealing cards and determining the initial turn.
        """

        self.__deck.shuffle()
        self.__deal_cards()
        self.__determine_initial_turn()

    @property
    def turn(self) -> Turn:
        """
        Current turn of the game.

        :return: Current turn instance.
        """

        return self.__current_turn

    @property
    def board(self) -> List[List[bool]]:
        return self.__board.matrix

    def play_card(self, card: Card) -> None:
        """
        Current player plays a card.

        :param card: Card instance to be played.
        """

        if Action.PLAY_CARD not in self.__current_turn.actions:
            raise ValueError(
                f"Invalid action in {self.__current_turn.actions}")

        if not self.__current_player.has_card(card):
            raise ValueError(f"Invalid card: {card}")

        self.__current_player.remove_card(card)
        self.__board.add_card(card)
        self.__advance_turn(Action.PLAY_CARD, card)

    def take_card(self) -> None:
        """
        Current player takes a card.
        """
        if Action.TAKE_CARD not in self.__current_turn.actions:
            raise ValueError(
                f"Invalid action in {self.__current_turn.actions}")

        self.__advance_turn(Action.TAKE_CARD, None)

    def give_card(self, card: Card) -> None:
        """
        Previous player gives a card.

        :param card: Card instance to be given.
        """

        if Action.GIVE_CARD not in self.__current_turn.actions:
            raise ValueError(
                f"Invalid action in {self.__current_turn.actions}")

        if not self.__current_turn.player.has_card(card):
            raise ValueError(f"Invalid card {card}")

        self.__current_turn.player.remove_card(card)
        self.__current_player.add_card(card)
        self.__advance_turn(Action.GIVE_CARD, card)

    def pass_turn(self) -> None:
        """
        Current player passes the turn.
        """

        if Action.PASS_TURN not in self.__current_turn.actions:
            raise ValueError(
                f"Invalid action in {self.__current_turn.actions}")

        self.__advance_turn(Action.PASS_TURN, None)

    @property
    def finished_players(self) -> List[Player]:
        """
        Get the list of players who have finished their cards, in the order they finished.

        :return: List of finished players.
        """
        return self.__finished_players

    def is_finished(self) -> bool:
        """
        Checks if the game is finished.

        The game is considered finished when the number of players who have finished playing their cards 
        is equal to the total number of players in the game.

        :return: True if the game is finished, False otherwise.
        """
        return len(self.finished_players) == len(self.__players)

    def __deal_cards(self) -> None:
        """
        Deal cards to all players one by one from the deck.
        """

        tmp_player_index: int = 0
        while (not self.__deck.empty()):
            card: Card = self.__deck.deal()
            self.__players[tmp_player_index].add_card(card)
            tmp_player_index = (tmp_player_index + 1) % len(self.__players)

    def __find_player_start_index(self) -> int:
        """
        Find the player who has the card 'Seven of Hearts' as the starting player.

        :return: Index of the starting player.
        """

        tmp_player_index: int = 0
        for player in self.__players:
            if (player.has_card(Card(Suit.HEARTS, Rank.SEVEN))):
                return tmp_player_index
            tmp_player_index = tmp_player_index + 1

        raise ValueError(f"Unable to determine player start index")

    def __determine_initial_turn(self) -> None:
        """
        Determine the initial turn of the game.
        """

        self.__current_player_index = self.__find_player_start_index()

        seven_of_hearts: Card = Card(Suit.HEARTS, Rank.SEVEN)

        if not self.__current_player.has_card(seven_of_hearts):
            raise ValueError(
                f"Unexpected error, initial player missing {seven_of_hearts}")

        self.__current_turn = Turn(
            [Action.PLAY_CARD], self.__current_player, [seven_of_hearts])

    def __advance_turn(self, action: Action, card: Card) -> None:
        """
        Advance the turn based on the given action and card. If the action involves playing or giving a card,
        checks whether the current player has no cards left and, if so, adds them to the list of finished players.

        :param action: Last action taken.
        :param card: Last card played or given card.
        """

        if action in [Action.PLAY_CARD, Action.GIVE_CARD] and len(self.__current_turn.player.hand) == 0:
            self.__finished_players.append(self.__current_turn.player)

        if len(self.__finished_players) == len(self.__players):
            return

        if action is Action.PLAY_CARD:
            self.__advance_turn_play_card(card)
        elif action is Action.TAKE_CARD:
            self.__advance_turn_take_card()
        else:
            self.__advance_turn_other()

    def __advance_turn_play_card(self, card: Card) -> None:
        """
        Handle the case when the last action was PLAY_CARD.

        :param card: The card being played
        """

        if card is None:
            raise ValueError("Unexpected error, card was not played")

        if (card.rank is Rank.ACE or card.rank is Rank.KING) and len(self.__current_player_valid_cards) > 0:
            self.__current_turn = Turn(
                [Action.PLAY_CARD, Action.PASS_TURN], self.__current_player, self.__current_player_valid_cards)
        else:
            self.__current_turn = Turn(
                [Action.PASS_TURN], self.__current_player, [])

    def __advance_turn_take_card(self) -> None:
        """
        Handle the case when the last action was TAKE_CARD.
        """

        self.__current_turn = Turn(
            [Action.GIVE_CARD], self.__previous_player, self.__previous_player.hand)

    def __advance_turn_other(self) -> None:
        """
        Handle the case when the last action was either GIVE_CARD nor PASS_TURN.
        """

        self.__advance_player()

        if len(self.__current_player_valid_cards) > 0:
            self.__current_turn = Turn(
                [Action.PLAY_CARD], self.__current_player, self.__current_player_valid_cards)
        else:
            self.__current_turn = Turn(
                [Action.TAKE_CARD], self.__current_player, [])

    @property
    def __current_player(self) -> Player:
        """
        Get the current player of the game.

        :return: Current player instance.
        """

        return self.__players[self.__current_player_index]

    @property
    def __current_player_valid_cards(self) -> List[Card]:
        """
        Get valid cards that the current player can play.

        :return: List of valid card instances.
        """

        return self.__board.get_valid_cards(self.__current_player.hand)

    @property
    def __previous_player(self) -> Player:
        """
        Get the previous player who has cards. Iterates backwards from the current player.
        Raises an exception if no such player is found after one full loop over the player list.

        :return: Previous player instance.
        """

        tmp_previous_player_index = self.__current_player_index
        for _ in range(len(self.__players)):
            tmp_previous_player_index = (
                tmp_previous_player_index - 1) % len(self.__players)
            if len(self.__players[tmp_previous_player_index].hand) > 0:
                return self.__players[tmp_previous_player_index]

        raise ValueError("No players with cards were found.")

    def __advance_player(self) -> None:
        """
        Advance the current player index until a player with cards is found.
        Raises an exception if no such player is found after one full loop over the player list.
        """

        for _ in range(len(self.__players)):
            self.__current_player_index = (
                self.__current_player_index + 1) % len(self.__players)
            if len(self.__current_player.hand) > 0:
                return

        raise ValueError("No players with cards were found.")
