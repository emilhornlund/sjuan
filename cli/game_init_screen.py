from enum import Enum, auto
from typing import List, Optional

from lib.player import PlayerType

from .screen import Screen

from lib.game import Game, PlayerInfo


class GameMode(Enum):
    SOLO = auto()
    PARTY = auto()


class GameInitScreen(Screen):
    """
    Game Initialization Screen class. This class is responsible for handling the game setup process.
    """

    def run(self) -> Game:
        """
        The main method of the class that manages the game setup process.

        :return: An instance of the Game class with the chosen game mode and players.
        """
        game_mode: Optional[GameMode] = None
        while game_mode is None:
            self.__print_screen(game_mode, None)
            game_mode = GameMode(self.get_number_input(
                "Choose the game mode (1-2): ", 1, 2))

        players_length: Optional[int] = None
        while players_length is None:
            self.__print_screen(game_mode, None)
            players_length = self.get_number_input(
                "Choose the number of players (3-8): ", 3, 8)

        player_infos: List[PlayerInfo] = []

        if game_mode is GameMode.PARTY:
            while len(player_infos) < players_length:
                self.__print_screen(game_mode, player_infos)
                human_player_name = input(
                    f"Choose the player's name ({len(player_infos) + 1}): ")
                player_infos.append(PlayerInfo(
                    name=human_player_name, type=PlayerType.HUMAN))
        else:
            human_player_name = input(
                f"Choose your name: ")
            player_infos.append(PlayerInfo(
                name=human_player_name, type=PlayerType.HUMAN))

            ai_player_names: List[str] = [
                "Bob", "Alice", "Ted", "Eve", "Frank", "Olivia", "Dave", "Wendy"]
            for index in range(1, players_length):
                ai_player_name = ai_player_names[index - 1]
                player_infos.append(PlayerInfo(
                    name=ai_player_name, type=PlayerType.AI))

        self.__print_screen(game_mode, player_infos)
        input("Press any key to start your new game")

        return Game(player_infos=player_infos)

    def __print_screen(self, game_mode: Optional[GameMode], player_infos: Optional[List[PlayerInfo]]) -> None:
        """
        Method to print the game setup screen based on the current state of game_mode and player_names.

        :param game_mode: The chosen game mode or None if no mode has been chosen yet.
        :param player_names: The list of player names or None if no players have been added yet.
        :return: None
        """
        if game_mode is None:
            self.print_menu_screen("New Game", "Mode", ["Solo", "Party"])
        elif player_infos is None:
            self.print_menu_screen("New Game", "Players", [])
        else:
            self.print_menu_screen("New Game", "Players", map(
                lambda player_info: f"{player_info.name} ({player_info.type})", player_infos))
