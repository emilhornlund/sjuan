from typing import List, Tuple

from lib.player import Player

from .screen import Screen

from lib.game import Game
from lib.card import Card
from lib.constants import Action, Suit, Rank


class GameScreen(Screen):
    """
    Game Screen class. This class is responsible for rendering the game board and handling player actions.
    """

    def __init__(self, game: Game) -> None:
        """
        Initialize GameScreen with a game instance.

        :param game: Game instance
        :return: None
        """

        self.__game = game

    def run(self) -> List[Player]:
        """
        The main method of the class that starts the game and handles turns.

        :return: List of finished players.
        """

        self.__game.start()

        while not self.__game.is_finished():
            self.__handle_turn()

        return self.__game.finished_players

    def __handle_turn(self) -> None:
        """
        Handles a single turn in the game.

        :return: None
        """

        self.clear()
        print(f"It's {self.__game.turn.player.name}'s turn.\n")
        actions = self.__get_turn_actions()
        self.__render(actions)
        action_index = self.get_number_input(
            f"Please select an action (1-{len(actions)}): ", 1, len(actions)) - 1
        self.__execute_action(actions[action_index])

    def __execute_action(self, action: Tuple[Action, Card]) -> None:
        """
        Executes the selected action.

        :param action: Tuple containing the selected action and a card if needed
        :return: None
        """

        if action[0] == Action.PLAY_ALL_CARDS:
            self.__game.play_all_cards()
        elif action[0] == Action.PLAY_CARD:
            self.__game.play_card(action[1])
        elif action[0] == Action.GIVE_CARD:
            self.__game.give_card(action[1])
        elif action[0] == Action.TAKE_CARD:
            self.__game.take_card()
        elif action[0] == Action.PASS_TURN:
            self.__game.pass_turn()

    def __get_turn_actions(self) -> List[Tuple[Action, Card]]:
        """
        Gets all the possible actions for the current turn.

        :return: List of possible actions
        """

        actions: List[Tuple[Action, Card]] = []
        for action in self.__game.turn.actions:
            if action is Action.PLAY_ALL_CARDS:
                actions.append((action, None))
            elif action is Action.PLAY_CARD:
                for card in self.__game.turn.valid_cards:
                    actions.append((action, card))
            elif action is Action.GIVE_CARD:
                for card in self.__game.turn.player.hand:
                    actions.append((action, card))
            elif action is Action.TAKE_CARD or action is Action.PASS_TURN:
                actions.append((action, None))
        return actions

    def __render(self, actions: List[Tuple[Action, Card]]) -> None:
        """
        Renders the game board, the player's hand, and the possible actions.

        :param actions: List of possible actions
        :return: None
        """

        output = ""
        output += "| Board                 | Hand                      | Actions                              |\n"
        output += "| --------------------- | ------------------------- | ------------------------------------ |\n"

        board_lines_tuple = self.__get_board_lines()
        board_lines = board_lines_tuple[0]
        board_max_line_width = board_lines_tuple[1]

        hand_lines_tuple = self.__get_hand_lines()
        hand_lines = hand_lines_tuple[0]
        hand_max_line_width = hand_lines_tuple[1]

        action_lines_tuple = self.__get_action_lines(actions)
        action_lines = action_lines_tuple[0]
        action_max_line_width = action_lines_tuple[1]

        max_lines = max(len(board_lines), len(hand_lines))

        for i in range(max_lines):
            if len(board_lines) > i:
                output += board_lines[i]
            else:
                output += "".ljust(board_max_line_width - 1)

            if len(hand_lines) > i:
                if len(board_lines) > i and board_lines[i][0] == "|":
                    output += hand_lines[i].lstrip("|")
                else:
                    output += hand_lines[i]
            else:
                output += "".ljust(hand_max_line_width)

            if len(action_lines) > i:
                if len(hand_lines) > i and hand_lines[i][0] == "|":
                    output += action_lines[i].lstrip("|")
                else:
                    output += action_lines[i]
            else:
                output += "".ljust(action_max_line_width)
            output += "\n"

        print(output)

    def __get_board_lines(self) -> Tuple[list[str], int]:
        """
        Gets the lines of the board that need to be printed.

        :return: Tuple containing a list of strings representing the board and the width of the board.
        """

        rank_symbols = {
            Rank.ACE: 'A', Rank.KING: 'K', Rank.QUEEN: 'Q', Rank.JACK: 'J',
            Rank.TEN: '10', Rank.NINE: '9', Rank.EIGHT: '8', Rank.SEVEN: '7',
            Rank.SIX: '6', Rank.FIVE: '5', Rank.FOUR: '4', Rank.THREE: '3', Rank.TWO: '2'
        }

        output = "|  ♥  |  ♦  |  ♣  |  ♠  |\n| --- | --- | --- | --- |\n"

        # Print the highest rank card for each suit
        for suit in Suit:
            rank_text = ""
            for i in range(Rank.KING.value, Rank.SEVEN.value, -1):
                if self.__game.board[suit.value - 1][i - 1]:
                    rank_text = f"{rank_symbols[Rank(i)]}  " if Rank.TEN != Rank(
                        i) else "10 "
                    break
            output += f"|  {rank_text}" if rank_text else "|     "
        output += "|\n"

        # Print the Seven of each suit, if it has been played
        for suit in Suit:
            output += f"|  7  " if self.__game.board[suit.value -
                                                     1][Rank.SEVEN.value - 1] else "|     "
        output += "|\n"

        # Print the lowest rank card for each suit
        for suit in Suit:
            rank_text = ""
            for i in range(Rank.ACE.value, Rank.SEVEN.value):
                if self.__game.board[suit.value - 1][i - 1]:
                    rank_text = f"{rank_symbols[Rank(i)]}  "
                    break
            output += f"|  {rank_text}" if rank_text else "|     "
        output += "|\n"
        output += "| --- | --- | --- | --- |"
        return (output.splitlines(), 25)

    def __get_hand_lines(self) -> Tuple[list[str], int]:
        """
        Gets the lines of the hand that need to be printed.

        :return: Tuple containing a list of strings representing the hand and the width of the hand.
        """

        max_line_width = 0
        output = ""
        for card in self.__game.turn.player.hand:
            tmp = f"{card.rank.name} of {card.suit.name}"
            max_line_width = max(max_line_width, len(tmp))
            output += f"| {tmp.ljust(25)} |\n"
        return (output.splitlines(), 27)

    def __get_action_lines(self, actions: List[Tuple[Action, Card]]) -> Tuple[list[str], int]:
        """
        Gets the lines of the actions that need to be printed.

        :param actions: List of possible actions
        :return: Tuple containing a list of strings representing the actions and the width of the actions.
        """

        output = ""
        for i, action in enumerate(actions):
            tmp = ""
            if action[0] == Action.PLAY_ALL_CARDS:
                tmp = f"Play all cards"
            elif action[0] == Action.PLAY_CARD:
                tmp = f"Play {action[1].rank.name} of {action[1].suit.name}"
            elif action[0] == Action.GIVE_CARD:
                tmp = f"Give {action[1].rank.name} of {action[1].suit.name}"
            elif action[0] == Action.TAKE_CARD:
                tmp = f"Take card"
            elif action[0] == Action.PASS_TURN:
                tmp = f"Pass turn"
            else:
                raise ValueError("Unknown action")
            tmp = f"({i + 1}) {tmp}"
            output += f"| {tmp.ljust(36)} |\n"
        return (output.splitlines(), 40)
