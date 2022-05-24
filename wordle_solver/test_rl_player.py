"""Test player winning rate."""

import sys
from datetime import datetime
from configparser import ConfigParser
import pandas as pd
from tensorflow import keras
from lib.game import Game
from lib.rl_strategy_player import RLStrategyPlayer

DATA_PATH = r"wordle_solver\datasets\words"
SUMMARY_PATH = r"wordle_solver\summary"

NUM_OOV_BUCKETS = 4 # Used in construct reinforcement learning player

def main(config_file=r"wordle_solver\test_rl_setup.ini"):
    start_time = datetime.now()
    time_stamp = start_time.strftime("%Y%m%d_%H%M%S")
    log_file = r"wordle_solver\log\test_rl_player_{0}.log".format(time_stamp)
    log = open(log_file, "a")

    config = ConfigParser()
    config.read(config_file)

    bag_word = pd.read_csv(config["common"]["path_bag_words"])
    random_state_game = config.getint("common", "random_state_game")
    random_state_player = config.getint("common", "random_state_player")
    num_testing_rounds = config.getint("common", "num_testing_rounds")
    game_play_verbose = config.getboolean("common", "game_play_verbose")

    model_path = config["common"]["model"]

    model = keras.models.load_model(model_path)

    game = Game(True, random_state_game)
    rl_player = RLStrategyPlayer(random_state_player, model, NUM_OOV_BUCKETS)
    game.set_bag_words(bag_word)
    rl_player.set_bag_words(bag_word)
    game_won_count = 0
    for _ in range(num_testing_rounds):
        game_won_count += game.play(rl_player, game_play_verbose)
        rl_player.reset_status()
    game_won_ratio = game_won_count / num_testing_rounds

    sys.stdout = log
    print(f"Tested model: {model_path}")
    testing_message = (
        f"Played {num_testing_rounds} rounds, Won {game_won_count} Rounds, "
        f"Win Ratio = {game_won_ratio}")
    print(testing_message)
    end_time = datetime.now()
    print("Testing Time: {}".format(end_time - start_time))
    log.close()

if __name__ == "__main__":
    main(*sys.argv[1:])