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

        # Initialize your environment with the defined game
        env = GameEnv(game)

        # Load the trained agent
        model = PPO.load("ppo_agent")

        # Initialize stats for players
        stats = [0]*len(env.game.players)

        for i in range(100):  # Play 100 games
            # Reset the environment before each game
            obs = env.reset()
            done = False
            while not done:
                # The agent chooses the action based on the current observation
                action, _states = model.predict(obs, deterministic=True)
                # Execute the chosen action in the environment
                obs, reward, done, info = env.step(action)

            # Find the position of our agent in the finished players list
            finish_index = env.game.finished_players.index(env.game.players[0])
            # Increment the corresponding index in the stats
            stats[finish_index] = stats[finish_index] + 1

        # Print the stats
        print("Stats:")
        for i, count in enumerate(stats):
            print(f"{i + 1}. {count / 100}")

    except KeyboardInterrupt:
        # Graceful shutdown on keyboard interrupt
        print("\nQuiting...")
        sys.exit(0)
