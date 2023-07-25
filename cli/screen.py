from abc import ABC, abstractmethod
from os import system, name
from typing import List, NoReturn


class Screen(ABC):
    """
    Abstract base class for all game screens.
    """

    @abstractmethod
    def run(self) -> NoReturn:
        """
        Abstract method to be implemented by subclasses. 
        This method will contain the main logic of each individual screen.

        :return: NoReturn
        """

        pass

    def get_number_input(self, title: str, start: int, end: int) -> int:
        """
        Get a number input from the user within a specified range.

        :param title: The prompt to be displayed to the user.
        :param start: The starting number (inclusive) of the valid range.
        :param end: The ending number (inclusive) of the valid range.
        :return: The valid number entered by the user.
        """

        value = None
        while value is None:
            value = input(title)
            if value == '' and start == 1 and end == 1:
                return 1
            else:
                try:
                    value = int(value)
                    if not start <= value <= end:
                        value = None  # reset value if it's not within the valid range
                except ValueError:
                    value = None  # reset value if it's not a valid integer
        return value

    def print_menu_screen(self, title: str, options_title: str, options: List[str]) -> NoReturn:
        """
        Print a menu screen with a title, options title, and a list of options.

        :param title: The title of the screen.
        :param options_title: The title of the options section.
        :param options: The list of options to be displayed.
        :return: NoReturn
        """

        self.clear()
        print("************************************")
        print(f"* {title.ljust(32)} *")
        print("*                                  *")
        print(f"* {options_title.ljust(32)} *")
        for i, option in enumerate(options):
            text = f"{i + 1}. {option}"
            print(f"* {text.ljust(32)} *")
        print("************************************\n")

    def clear(self) -> NoReturn:
        """
        Clear the console screen. 
        This is OS dependent ('cls' for Windows, 'clear' for Unix systems).

        :return: NoReturn
        """

        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
