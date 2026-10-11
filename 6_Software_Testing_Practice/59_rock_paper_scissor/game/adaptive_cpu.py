import random
from collections import deque


class AdaptiveCPU:
    # Maps each move to the move that beats it
    COUNTER = {
        "ROCK": "PAPER",
        "PAPER": "SCISSORS",
        "SCISSORS": "ROCK",
    }

    def __init__(self, choices, history_size=8, adapt_strength=0.6, min_history=3):
        """
        history_size:   how many recent player moves to remember
        adapt_strength: 0.0 = pure random, 1.0 = always counter the player's distribution
        min_history:    moves needed before adaptation kicks in
        """
        self.choices = list(choices)
        self.history = deque(maxlen=history_size)
        self.adapt_strength = adapt_strength
        self.min_history = min_history

    def reset(self):
        self.history.clear()

    def record(self, player_move):
        self.history.append(player_move)

    def move_weights(self):
        n = len(self.choices)
        if len(self.history) < self.min_history:
            return {c: 1 / n for c in self.choices}

        total = len(self.history)
        freq = {c: 0 for c in self.choices}
        for move in self.history:
            freq[move] += 1

        # Random floor shared evenly, plus a share that follows the player's habits
        weights = {c: (1 - self.adapt_strength) / n for c in self.choices}
        for player_move, count in freq.items():
            weights[self.COUNTER[player_move]] += self.adapt_strength * count / total
        return weights

    def choose(self):
        weights = self.move_weights()
        return random.choices(self.choices, weights=[weights[c] for c in self.choices])[0]