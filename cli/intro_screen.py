from enum import Enum

from .screen import Screen


class IntroScreenChoice(Enum):
    """
    Enum class representing the options on the intro screen.
    """

    NEW_GAME = 1
    RULES = 2
    EXIT = 3


class IntroScreen(Screen):
    """
    Screen class representing the intro screen of the game.
    """

    def run(self) -> IntroScreenChoice:
        """
        Runs the intro screen by displaying the menu options 
        and getting the user's choice. This function is called 
        to transition to the next screen based on the user's choice.

        :return: An IntroScreenChoice enum value representing the user's choice.
        """

        self.print_menu_screen("Welcome to the Sjuan Card Game!", "Menu", [
            "New Game", "View Rules", "Exit"])

        return IntroScreenChoice(self.get_number_input(
            "Please select an option (1-3): ", 1, 3))
