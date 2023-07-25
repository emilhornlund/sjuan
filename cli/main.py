from .game_init_screen import GameInitScreen
from .game_rules_screen import GameRulesScreen
from .game_screen import GameScreen
from .intro_screen import IntroScreen, IntroScreenChoice


def main() -> None:
    """
    Main function that runs the card game application. It manages the transitions 
    between different screens based on user's choices until the user chooses to exit 
    the game or a KeyboardInterrupt is raised.

    :return: None
    """

    screen = None
    while screen is None:
        # Initialize and run the IntroScreen
        screen = IntroScreen()
        choice = screen.run()

        if choice is IntroScreenChoice.NEW_GAME:
            # If the user chose "New Game", initialize and run the GameInitScreen
            screen = GameInitScreen()
            game = screen.run()

            # Then initialize and run the GameScreen with the created game
            screen = GameScreen(game)
            screen.run()

        if choice is IntroScreenChoice.RULES:
            # If the user chose "View Rules", initialize and run the GameRulesScreen
            screen = GameRulesScreen()
            screen.run()

        if choice is not IntroScreenChoice.EXIT:
            # If the user did not choose "Exit", return to the IntroScreen
            screen = None


if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuiting...")
        sys.exit(0)
