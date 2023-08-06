import mmh3
import math
from statistics import median


class BJKST:
    def __init__(self, epsilon=0.05, delta=0.05, c=1, hash_type="mmh3",
                 seed=42):
        self.depth = c*int(math.log(1/delta, 2))
        self.epsilon = epsilon
        self.hash_type = hash_type

        # t ~ 2/eps^2
        self.t = c*int(math.pow(1/self.epsilon, 2))

        # data structure to store the smallest t hash values
        self.B = [dict() for _ in range(self.depth)]
        self.z = [0 for _ in range(self.depth)]
        self.max_32_int = pow(2, 32) - 1

        self.seeds_h = [0 for _ in range(self.depth)]

        for i in range(self.depth):
            self.seeds_h[i] = i*i*seed

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        if self.hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False)

    @staticmethod
    def zeros(hash_value):
        r = 1
        divisor = math.pow(2, r)
        while hash_value % divisor == 0:
            r += 1
            divisor *= 2
        return r-1

    def insert(self, token):
        """ Insert a token into the sketch. Token must be byte-like objects. """
        for i in range(self.depth):
            hash_value_h = self._hash(token, self.seeds_h[i])
            hash_value_g = hash_value_h/self.max_32_int
            tail_length = BJKST.zeros(hash_value_h)
            if tail_length >= self.z[i]:
                self.B[i][hash_value_g] = tail_length
                if len(self.B[i].keys()) >= self.t:
                    self.z[i] += 1
                    elements_to_remove = []
                    for key, tail_length in self.B[i].items():
                        if tail_length < self.z[i]:
                            elements_to_remove.append(key)
                    for element in elements_to_remove:
                        del self.B[i][element]

    def estimator(self):
        """ Return the estimate for the number of distinct
        elements inserted so far """
        est = []
        for i in range(self.depth):
            b_length = len(self.B[i])
            two_multiplier = math.pow(2, self.z[i])
            est.append(b_length * two_multiplier)
        median_of_est = median(est)
        return median_of_est