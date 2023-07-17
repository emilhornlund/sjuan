![github actions workflow](https://github.com/emilhornlund/sjuan/actions/workflows/python-ci.yml/badge.svg)

# Sjuan - A Card Game Swedish Style

Sjuan is a Swedish card game for 3-8 players. This command line program provides a digital version of the game, allowing you to play with computer opponents or with friends on the same device.

## Game Overview

The game is played with a standard deck of cards, with the goal being to build sequences from the sevens in each suit and be the first to rid of all your cards. It's a simple, yet strategic game that's suitable for players of all ages.

## How to Play

### Game Preparations

The game starts by dealing all the cards to the players.

### Game Play

The player who has the 7 of hearts starts the game. On their turn, a player must either:

- Place a 6 or 8 of the same suit on the corresponding 7.
- Place another 7 on the table.

The four 7's are placed next to each other. On one side of the 7's, the 8's are placed, then the 9's, and so on up to the Kings. On the other side, the 6's are placed, then the 5's, and so on down to the Aces. Players must always follow the suit.

If a player cannot play a card, the previous player passes a card of their choice to this player. If a player plays an Ace or a King, they may place another card if they wish.

### Winning the Game

The player who first gets rid of all their cards wins. If a player can play all their remaining cards in a single turn, they do so and win the game.

## Installation and Usage

*(Provide instructions here on how to install and run your game, including any necessary prerequisites like Python version or libraries)*

## Running Tests

This project uses pytest for testing. Follow these steps to run the tests:

1. Ensure you have pytest installed in your virtual environment. If not, you can install it with pip:

```bash
pip install pytest
```

2. To run all tests, navigate to the project directory in your terminal and use the `pytest` command:

```bash
pytest
```

3. If you want to run a specific test file, you can specify it like this:

```bash
pytest tests/test_file.py
```

Replace `test_file.py` with the name of the test file you want to run.

## Contributing

We welcome contributions to this project! Please read our contributing guide for details on how to contribute.

## License

Sjuan is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
