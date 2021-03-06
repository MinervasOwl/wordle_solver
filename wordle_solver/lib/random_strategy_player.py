"""The player using random strategy for Wordle."""

import random
from string import ascii_lowercase
from lib.player import Player

class RandomStrategyPlayer(Player):
    """A player of wordle game that uses randomized strategy"""
    def __init__(self, use_fixed_seed=False, random_state=None,
                 perturbation_rate=0):
        Player.__init__(self)
        self.use_fixed_seed = use_fixed_seed
        self.random_state = random_state
        self.word_index = {}
        self.possible_guess_indices = set()
        self.previous_guess = None
        self.perturbation_rate = perturbation_rate

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        Player.set_bag_words(self, bag_words)
        self.build_word_index()

    def build_word_index(self):
        set_ascii_lowercase = set(ascii_lowercase)
        for letter in ascii_lowercase:
            for i in range(5):
                for clue in ["0", "1", "2"]:
                    self.word_index[(letter, i, clue)] = set()
        for index, row in self.bag_words.iterrows():
            letters_in_word = set(row["word"])
            for i in range(5):
                self.word_index[row["word"][i], i, "2"].add(index)
                for letter in letters_in_word.difference(row["word"][i]):
                    self.word_index[letter, i, "1"].add(index)
                for letter in set_ascii_lowercase.difference(row["word"][i]):
                    self.word_index[letter, i, "0"].add(index)

    def print_word_index(self, verbose=False):
        if verbose:
            print(self.word_index)
        else:
            for word, indices in self.word_index.items():
                if len(indices) > 0:
                    print(f"{word}: {indices}")

    def gen_guess(self, state, verbose=False):
        "generate a guess"
        if self.use_fixed_seed:
            new_random_state = self.random_state + state.num_guesses
            random.seed(new_random_state)
        else:
            random.seed()
        if state.num_guesses == 0:
            self.possible_guess_indices = set(self.bag_words.index)
            guess_index = random.choice(tuple(self.bag_words.index))
            guess = (self.bag_words.loc[guess_index, "word"])
            self.previous_guess = guess
        else:
            for i, x in enumerate(state.hints[-1]):
                possible_indices = self.word_index[self.previous_guess[i], i, x]
                self.possible_guess_indices = (
                    self.possible_guess_indices & possible_indices)
            if verbose:
                print(f"Possible Indices: {self.possible_guess_indices}")
            if random.uniform(0, 1) < self.perturbation_rate:
                guess_index = random.choice(tuple(self.bag_words.index))
                guess = (self.bag_words.loc[guess_index, "word"])
            else:
                guess_index = random.choice(tuple(self.possible_guess_indices))
                guess = (self.bag_words.loc[guess_index, "word"])

            self.previous_guess = guess
        return guess
