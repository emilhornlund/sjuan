from typing import List, Optional, NoReturn

from .screen import Screen

from lib.game import Game, GameMode


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

        player_names: List[str] = []
        while len(player_names) < players_length:
            self.__print_screen(game_mode, player_names)
            player_name = input(
                f"Choose the player's name ({len(player_names) + 1}): ")
            player_names.append(player_name)

        self.__print_screen(game_mode, player_names)
        input("Press any key to start your new game")

        return Game(game_mode, player_names)

    def __print_screen(self, game_mode: Optional[GameMode], player_names: Optional[List[str]]) -> NoReturn:
        """
        Method to print the game setup screen based on the current state of game_mode and player_names.

        :param game_mode: The chosen game mode or None if no mode has been chosen yet.
        :param player_names: The list of player names or None if no players have been added yet.
        :return: NoReturn
        """
        if game_mode is None:
            self.print_menu_screen("New Game", "Mode", ["Solo", "Party"])
        elif player_names is None:
            self.print_menu_screen("New Game", "Players", [])
        else:
            self.print_menu_screen("New Game", "Players", player_names)
