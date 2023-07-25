from typing import List, NoReturn

from lib.player import Player

from .screen import Screen


class GameOverScreen(Screen):
    """
    Class that represents the game over screen.
    """

    def __init__(self, finished_players: List[Player]) -> None:
        """
        Initialize GameOverScreen with the list of players who have finished the game.

        :param finished_players: List of players who have finished the game.
        :return: None
        """

        super().__init__()

        self.__finished_players: List[Player] = finished_players

    def run(self) -> None:
        """
        Display the game over screen with the names and types of players who have finished the game.
        The user is then prompted to press any key to continue.

        :return: None
        """

        self.print_menu_screen("Game Over", "Podium:", map(
            lambda player: f"{player.name} ({player.type})", self.__finished_players))

        input("Press any key to continue")
