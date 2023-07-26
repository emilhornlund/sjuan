import unittest
import numpy as np

from ai.game_env import GameEnv
from lib.card import Card, Rank, Suit
from lib.action import Action, ActionType
from lib.game import Game, PlayerInfo
from lib.player import PlayerType


class TestGameEnv(unittest.TestCase):

    def setUp(self):
        self.game = Game(player_infos=[
            PlayerInfo(name="Gym", type=PlayerType.HUMAN),
            PlayerInfo(name="Alice", type=PlayerType.AI),
            PlayerInfo(name="Ted", type=PlayerType.AI),
            PlayerInfo(name="Eve", type=PlayerType.AI)])
        self.env = GameEnv(self.game)

    def test_step_invalid_action(self):
        self.env.reset()

        # Make an action that's not available in the current state
        # Use a number larger than the size of action space to ensure it's invalid
        action = self.env.action_space.n  # Change from "n - 1" to "n"
        with self.assertRaises(IndexError):
            observation, reward, done, info = self.env.step(action)

    def test_step_valid_action(self):
        self.env.reset()

        # Choose an action that is valid in the initial state
        action = 0
        for i, act in enumerate(self.env.all_possible_actions):
            if act in self.env.game.turn.actions:
                action = i
                break

        observation, reward, done, info = self.env.step(action)

        # For a valid action, the reward should not be a penalty
        # Whether the game ends or not depends on the specific action and game rules
        self.assertNotEqual(reward, -1.0)

    def test_reset(self):
        initial_state = self.env.reset()
        # Verify the type of state
        self.assertIsInstance(initial_state, np.ndarray)
        # Verify the size of state
        self.assertEqual(len(initial_state),
                         self.env.observation_space.shape[0])

    def test_render(self):
        self.env.reset()
        # Simply call the function to verify it doesn't cause an error
        self.env.render()

    # Add more tests for each function in your environment as necessary
    # You might also want to add tests that play through an entire game to verify the overall game flow


if __name__ == "__main__":
    unittest.main()
