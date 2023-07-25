# lib/game.py

from typing import List, NamedTuple, Optional, Set


from .action_decider import ActionDecider
from .action import Action, ActionType
from .board import Board
from .card import Card
from .constants import Suit, Rank
from .deck import Deck
from .player import Player, PlayerType
from .turn import Turn


class PlayerInfo(NamedTuple):
    name: str
    type: PlayerType


class Game:
    """
    Main Game class that encapsulates all the game logic.
    """

    def __init__(self, player_infos: List[PlayerInfo]) -> None:
        """
        Constructor for the Game class.

        :param player_names: List of player names.
        :return: None
        """

        self.__player_infos: List[PlayerInfo] = player_infos
        self.__finished_players: List[Player] = []
        self.reset()

    def reset(self) -> None:
        """
        Reset the game, initialize players, deck, board and current turn.

        :return: None
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

        :return: None
        """

        self.__deck.shuffle()
        self.__deal_cards()
        self.__start_turn()

    @property
    def turn(self) -> Turn:
        """
        Current turn of the game.

        :return: Current turn instance.
        """

        return self.__current_turn

    @property
    def board(self) -> List[List[bool]]:
        """
        Get the current state of the board.

        :return: A 2D matrix representing the current state of the board.
        """

        return self.__board.matrix

    def execute_action(self, action: Action) -> None:
        """
        Execute a given action in the game.

        :param action: An Action object representing the action to be performed.
        :return: None
        """

        self.__validate_action(action=action)

        if action.type is ActionType.PLAY_ALL_CARDS:
            for card in self.__current_player.hand:
                self.__current_player.remove_card(card=card)
                self.__board.add_card(card=card)

        elif action.type is ActionType.PLAY_CARD:
            self.__current_player.remove_card(card=action.card)
            self.__board.add_card(card=action.card)

        elif action.type is ActionType.GIVE_CARD:
            self.__current_turn.player.remove_card(action.card)
            self.__current_player.add_card(action.card)

        self.__advance_turn(action=action)

    @property
    def finished_players(self) -> List[Player]:
        """
        Get a list of players who have finished the game.

        :return: A list of Player objects who have finished the game.
        """

        return self.__finished_players

    def is_finished(self) -> bool:
        """
        Check whether the game is finished or not.

        :return: True if the game is finished, False otherwise.
        """

        return len(self.finished_players) == len(self.__players)

    def __validate_action(self, action: Action) -> None:
        """
        Validate the given action.

        :param action: An Action object representing the action to be validated.
        :return: None
        """

        if not self.__current_turn.has_action(action=action):
            raise ValueError(f"Invalid action {action}")

        if action.type in {ActionType.PLAY_CARD, ActionType.GIVE_CARD}:
            if not action.card:
                raise ValueError(f"Invalid action {action.type} without card")
            elif (action.type is ActionType.PLAY_CARD and not self.__current_player.has_card(card=action.card)) or (action.type is ActionType.GIVE_CARD and not self.__current_turn.player.has_card(card=action.card)):
                raise ValueError(
                    f"Invalid card {action.card} for action {action.type}")
        else:
            if action.type is ActionType.PLAY_ALL_CARDS and not self.__is_current_player_all_cards_valid():
                raise ValueError(f"Invalid action {action.type}")
            elif action.card:
                raise ValueError(
                    f"Invalid card {action.card} for action {action.type}")

    def __deal_cards(self) -> None:
        """
        Deal cards to all players one by one from the deck.

        :return: None
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

    def __start_turn(self) -> None:
        """
        Starts the first turn of the game.

        :return: None
        """

        self.__current_player_index = self.__find_player_start_index()

        seven_of_hearts: Card = Card(Suit.HEARTS, Rank.SEVEN)

        if not self.__current_player.has_card(seven_of_hearts):
            raise ValueError(
                f"Unexpected error, initial player missing {seven_of_hearts}")

        actions: Set[Action] = set()
        actions.add(Action(type=ActionType.PLAY_CARD, card=seven_of_hearts))

        self.__current_turn = Turn(
            actions=actions, player=self.__current_player)

        if self.__current_turn.player.type is PlayerType.AI:
            self.__advance_turn_decision()

    def __advance_turn(self, action: Action) -> None:
        """
        Advance the turn based on the given action.

        :param action: An Action object representing the last action taken.
        :return: None
        """

        if action.type in {ActionType.PLAY_CARD, ActionType.PLAY_ALL_CARDS, ActionType.GIVE_CARD} and not self.__current_turn.player.hand:
            self.__finished_players.append(self.__current_turn.player)

        if len(self.__finished_players) == len(self.__players):
            return

        if action.type is ActionType.PLAY_CARD:
            if action.card is None:
                raise ValueError("Unexpected error, card was not played")
            self.__advance_turn_play_card(card=action.card)
        elif action.type is ActionType.TAKE_CARD:
            self.__advance_turn_take_card()
        else:
            self.__advance_turn_other()

        if self.__current_turn.player.type is PlayerType.AI:
            self.__advance_turn_decision()

    def __advance_turn_play_card(self, card: Card) -> None:
        """
        Handle the case when the last action was PLAY_CARD.

        :param card: A Card object representing the last card played.
        :return: None
        """

        if card is None:
            raise ValueError("Unexpected error, card was not played")

        actions: Set[Action] = set()

        if (card.rank is Rank.ACE or card.rank is Rank.KING) and len(self.__current_player_valid_cards) > 0:
            if self.__is_current_player_all_cards_valid():
                actions.add(Action(type=ActionType.PLAY_ALL_CARDS))
            for card in self.__current_player_valid_cards:
                actions.add(Action(type=ActionType.PLAY_CARD, card=card))

        actions.add(Action(type=ActionType.PASS_TURN))

        self.__current_turn = Turn(
            actions=actions, player=self.__current_player)

    def __advance_turn_take_card(self) -> None:
        """
        Handle the case when the last action was TAKE_CARD.

        :return: None
        """

        actions: Set[Action] = set()
        for card in self.__previous_player.hand:
            actions.add(Action(type=ActionType.GIVE_CARD, card=card))

        self.__current_turn = Turn(
            actions=actions, player=self.__previous_player)

    def __advance_turn_other(self) -> None:
        """
        Handle the case when the last action was neither PLAY_CARD nor TAKE_CARD.

        :return: None
        """

        self.__advance_player()

        actions: Set[Action] = set()

        if len(self.__current_player_valid_cards) > 0:
            if self.__is_current_player_all_cards_valid():
                actions.add(Action(type=ActionType.PLAY_ALL_CARDS))
            for card in self.__current_player_valid_cards:
                actions.add(Action(type=ActionType.PLAY_CARD, card=card))
        else:
            actions.add(Action(type=ActionType.TAKE_CARD))

        self.__current_turn = Turn(
            actions=actions, player=self.__current_player)

    def __advance_turn_decision(self) -> None:
        """
        Execute the action decision making for the current turn.

        :return: None
        """

        action = ActionDecider.decide_action(
            self.__board.matrix, self.__current_turn)
        self.execute_action(action)

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
        Get a list of valid cards that the current player can play.

        :return: A list of Card objects that the current player can play.
        """

        return self.__board.get_valid_cards(self.__current_player.hand)

    def __is_current_player_all_cards_valid(self) -> bool:
        """
        Check whether all the cards of the current player are valid or not.

        :return: True if all the cards of the current player are valid, False otherwise.
        """

        return self.__board.get_valid_cards(self.__current_player.hand) == self.__current_player.hand

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
        Move the turn to the next player.

        :return: None
        """

        for _ in range(len(self.__players)):
            self.__current_player_index = (
                self.__current_player_index + 1) % len(self.__players)
            if len(self.__current_player.hand) > 0:
                return

        raise ValueError("No players with cards were found.")
