import mmh3
import math
import random
from collections import defaultdict


class MinHash:
    def __init__(self, epsilon=0.2, delta=0.05, c=2, hash_type="mmh3", r=3, b=62):
        """ epsilon: relative error, delta: failure probability
        for each hash function h, maintain the smallest hash value H """

        self.seed = []
        self.sets = dict()

        self.k = int(c * math.ceil(1/(epsilon * epsilon)) *
                     math.log(c/delta, math.e))
        self.k = 186
        self.hash_type = hash_type

        self.seed_range = int(math.pow(self.k, 2))
        self.max_128_int = pow(2, 128)-1
        self.max_32_int = pow(2, 32)-1

        # initialize the seeds for hash functions
        self.seed = [random.randint(1, self.seed_range) for _ in range(self.k)]

        self.b = b
        self.r = r
        self.lsh_seed = [random.randint(1, self.seed_range) for _ in range(self.b)]
        self.bands = dict()
        self.neighborhoods = defaultdict(set)

    def _hash128(self, token, seed):
        """ Compute the hash of a token. """
        if self.hash_type == "mmh3":
            return mmh3.hash128(token, seed, signed=False)/self.max_128_int

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        if self.hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False)/self.max_32_int

    def insert(self, set_name, token):
        """ Insert a token into the sketch. Token must be byte-like objects."""
        if set_name not in self.sets:
            self.sets[set_name] = [1 for _ in range(self.k)]
        for i in range(self.k):
            hash_value = self._hash(token, self.seed[i])
            if hash_value < self.sets[set_name][i]:
                self.sets[set_name][i] = hash_value

    def measure_jaccard_distance(self, set1, set2):
        match = 0
        for i in range(self.k):
            set1_smallest_hash = self.sets[set1][i]
            set2_smallest_hash = self.sets[set2][i]
            if set1_smallest_hash == set2_smallest_hash:
                match += 1
        jaccard_estimate = match / self.k
        return jaccard_estimate

    def create_jaccard_grid(self):
        set_names = list(self.sets.keys())
        set_count = len(set_names)

        grid = [[0 for set_name in set_names] for set_name in set_names]
        max_overlap = {"SetA": "", "SetB": "", "Dist": 0}

        for setA in range(set_count):
            for setB in range(setA, set_count):
                dist = self.measure_jaccard_distance(set_names[setA], set_names[setB])
                if dist > max_overlap["Dist"] and dist < 1:
                    max_overlap["SetA"] = set_names[setA]
                    max_overlap["SetB"] = set_names[setB]
                    max_overlap["Dist"] = dist
                grid[setA][setB] = dist
                grid[setB][setA] = grid[setA][setB]

        return grid, max_overlap

    def divide_list_into_chunks(self, key, r, b):
        hashed_chunk_list = []
        signature = self.sets[key]
        for i in range(0, b):
            x = i * r
            chunk = signature[x: x+r]
            chunk = str(chunk)
            chunk_hash = self._hash(chunk, self.lsh_seed[i])
            self.neighborhoods[chunk_hash].add(key)
            hashed_chunk_list.append(chunk_hash)
        return hashed_chunk_list

    def create_bands_for_lsh(self, r, b):
        self.neighborhoods = defaultdict(set)
        for key in self.sets.keys():
            split_signature = self.divide_list_into_chunks(key, r, b)
            self.bands[key] = split_signature
