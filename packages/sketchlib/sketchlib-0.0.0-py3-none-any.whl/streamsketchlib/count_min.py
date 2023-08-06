from math import ceil, inf, pow, log
import mmh3


class CountMin:
    max_32_int = pow(2, 32) - 1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.05, seed=10):
        self.epsilon = epsilon
        self.phi = phi
        self.delta = delta
        self.epsilon_star = self.phi * self.epsilon
        self.width = ceil(1/self.epsilon_star)
        self.depth = ceil(log(1/self.delta))
        self.table = [[0 for _ in range(self.width)]
                      for __ in range(self.depth)]
        self._hash_seeds = [0 for _ in range(self.depth)]

        for i in range(self.depth):
            self._hash_seeds[i] = i*i*seed

    @classmethod
    def from_existing(cls, original_cm):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm = cls()
        new_cm.epsilon = original_cm.epsilon
        new_cm.delta = original_cm.delta
        new_cm.width = original_cm.width
        new_cm.depth = original_cm.depth
        new_cm.table = [[0 for _ in range(new_cm.width)]
                        for __ in range(new_cm.depth)]
        new_cm._hash_seeds = original_cm._hash_seeds
        return new_cm

    def _hash(self, token, seed):
        """ Compute the hash of a token. Converts hash value to a bin number
            based on k."""
        hash_value = mmh3.hash(token, seed, signed=False)/self.max_32_int
        bin_number = hash_value * self.width
        return int(bin_number)

    def insert(self, token, count):
        for row in range(self.depth):
            col = self._hash(token, self._hash_seeds[row])
            self.table[row][col] = self.table[row][col] + count

    def estimate_count(self, token):
        estimate = inf
        for row in range(self.depth):
            col = self._hash(token, self._hash_seeds[row])
            estimate = min(estimate, self.table[row][col])
        return estimate

    def merge(self, other_count_min):
        row_count = len(self.table)
        col_count = len(self.table[0])

        for row in range(row_count):
            for col in range(col_count):
                self.table[row][col] += other_count_min.table[row][col]
