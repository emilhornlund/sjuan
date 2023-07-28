import gym
import numpy as np
from gym import spaces
from typing import List, Tuple

from lib.action import Action, ActionType
from lib.card import Card, Rank, Suit

from lib.game import Game


class GameEnv(gym.Env):
    """Custom Environment that follows gym interface. This is a wrapper over the game environment 
    and provides an interface for interacting with the game using the standard gym methods.
    """

    def __init__(self, game: Game) -> None:
        """
        Initialize the environment with the given game.

        :param game: the game to initialize the environment with.
        """

        super(GameEnv, self).__init__()

        # Total number of cards in a deck
        total_cards = 52

        # Create a list of all possible actions
        self.all_possible_actions: List[Action] = []
        for suit in Suit:
            for rank in Rank:
                card = Card(suit=suit, rank=rank)
                self.all_possible_actions.append(
                    Action(type=ActionType.PLAY_CARD, card=card))
                self.all_possible_actions.append(
                    Action(type=ActionType.GIVE_CARD, card=card))
        self.all_possible_actions += [
            Action(type=ActionType.PLAY_ALL_CARDS),
            Action(type=ActionType.TAKE_CARD),
            Action(type=ActionType.PASS_TURN)
        ]

        # Define the action and observation space
        self.action_space = spaces.Discrete(len(self.all_possible_actions))
        self.observation_space = spaces.Box(
            low=0,
            high=total_cards,
            shape=(total_cards * 2 + len(game.players) - 1,),
            dtype=np.int32
        )

        self.game = game
        self.game.start()

    def step(self, action: int) -> Tuple[np.array, float, bool, dict]:
        """
        Execute one time step within the environment. This method applies the action and returns the 
        resulting observation, reward, and whether the game is done.

        :param action: an action to apply to the environment.
        :return: tuple containing the new observation, reward, whether the game is done and extra info.
        """

        # Map to corresponding action
        initial_action_choice: Action = self.all_possible_actions[action]
        action_choice: Action = initial_action_choice

        # If the action isn't valid for this state, select a new action at random until a valid one is found
        if action_choice not in self.game.turn.actions:
            # Give a small negative reward for attempting an invalid action
            invalid_action_penalty = -0.01

            while action_choice not in self.game.turn.actions:
                action = self.action_space.sample()  # Sample a new action
                action_choice = self.all_possible_actions[action]
        else:
            # The initial action was valid, so there is no penalty
            invalid_action_penalty = 0

        # Calculate the reward for the final action (valid initial or sampled)
        reward = self.get_reward(action_choice) + invalid_action_penalty

        self.game.execute_action(action_choice)

        done = self.game.is_finished()
        if done:
            # Reward or penalty at the end of the game
            reward = self.get_reward(action_choice)

        return self.get_state(), reward, done, {}

    def reset(self) -> np.array:
        """
        Reset the state of the environment to an initial state.

        :return: initial state of the environment.
        """

        self.game.reset()
        self.game.start()
        return self.get_state()

    def render(self, mode='human') -> None:
        """
        Render the current state of the game environment to the console.

        :param mode: the mode to use for rendering.
        """

        print("\nGame Overview")
        self.__render_board()
        self.__render_finished_players()

    def get_reward(self, action_choice: Action):
        """
        Calculate and return the reward for the given action.

        :param action_choice: the action to get the reward for.
        :return: the reward for the given action.
        """

        if self.game.is_finished():
            if self.game.finished_players[0] == self.game.players[0]:
                return 1.0
            else:
                return -1.0
        else:
            return 0  # default case (should ideally never be reached)

    def get_state(self) -> np.array:
        """
        Return the current state of the game environment.

        :return: the current state of the game environment.
        """

        # Flatten the board into a single list.
        board_encoding = [card for suit in self.game.board for card in suit]

        # One-hot encode the hand.
        hand_encoding = [0]*52
        for card in self.game.turn.player.hand:
            hand_encoding[self.__card_to_index(card)] = 1

        # Get the number of cards in each opponent's hand.
        opponent_hand_sizes = [len(opponent.hand)
                               for opponent in self.game.turn.opponents]

        # Combine the encodings into a single list and return it.
        return np.array(board_encoding + hand_encoding + opponent_hand_sizes)

    def __card_to_index(self, card: Card) -> int:
        """
        Convert a card to an index.

        :param card: the card to convert to an index.
        :return: the index of the card.
        """

        return (card.suit.value - 1) * 13 + (card.rank.value - 1)

    def __render_board(self) -> None:
        """
        Render the current state of the board to the console.
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
                if self.game.board[suit.value - 1][i - 1]:
                    rank_text = f"{rank_symbols[Rank(i)]}  " if Rank.TEN != Rank(
                        i) else "10 "
                    break
            output += f"|  {rank_text}" if rank_text else "|     "
        output += "|\n"

        # Print the Seven of each suit, if it has been played
        for suit in Suit:
            output += f"|  7  " if self.game.board[suit.value -
                                                   1][Rank.SEVEN.value - 1] else "|     "
        output += "|\n"

        # Print the lowest rank card for each suit
        for suit in Suit:
            rank_text = ""
            for i in range(Rank.ACE.value, Rank.SEVEN.value):
                if self.game.board[suit.value - 1][i - 1]:
                    rank_text = f"{rank_symbols[Rank(i)]}  "
                    break
            output += f"|  {rank_text}" if rank_text else "|     "
        output += "|\n"
        output += "| --- | --- | --- | --- |"
        print(output)

    def __render_finished_players(self) -> None:
        """
        Render the current state of the finished players to the console.
        """

        if len(self.game.finished_players) > 0:
            print("Finished players:")
            for i, player in enumerate(self.game.finished_players):
                print(f"{i + 1}. ${player.name}")
