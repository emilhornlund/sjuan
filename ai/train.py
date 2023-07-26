from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from ai.game_env import GameEnv
from lib.game import Game, PlayerInfo
from lib.player import PlayerType

if __name__ == "__main__":
    import sys
    try:
        # Define the game with players' information
        game = Game(player_infos=[
                    PlayerInfo(name="Agent", type=PlayerType.AGENT),
                    PlayerInfo(name="Alice", type=PlayerType.AI),
                    PlayerInfo(name="Ted", type=PlayerType.AI),
                    PlayerInfo(name="Eve", type=PlayerType.AI)])

        # Initialize your environment
        env = GameEnv(game)

        # Vectorized environments allow to easily multiprocess training
        # We only use one for this example hence the DummyVecEnv
        vec_env = DummyVecEnv([lambda: env])

        # Initialize the agent using PPO with a MLP (feed-forward neural network) policy
        model = PPO("MlpPolicy", vec_env, verbose=1)

        # Train the agent for specified timesteps
        model.learn(total_timesteps=10000, progress_bar=True)

        # Save the trained agent for future use
        model.save("ppo_agent")
    except KeyboardInterrupt:
        # Graceful shutdown on keyboard interrupt
        print("\nQuiting...")
        sys.exit(0)
