import mmh3
import math
import bisect
from bisect import bisect_left
import statistics


class F0Estimate:
    """
    Loglog algorithm: memory efficient data structure to estimate
    the number of distinct elements in streams
    """
    def __init__(self, epsilon=0.01, delta=0.01, c=2, hash_type="mmh3", seed=42):
        """ epsilon: relative error
        delta: failure probability
        This is the first algorithm of [BJKST02]
        """
        self.epsilon = epsilon
        self.hash_type = hash_type
        self.max_128_int = pow(2, 128)-1

        # width ~ c/eps^2 and depth ~ c log(1/delta)
        self.width = c*int(math.pow(1/self.epsilon, 2))
        self.depth = c*int(math.log(1/delta, 2))
        self.seeds = [seed*i for i in range(self.depth)]

        # data structure to store the smallest t hash values
        self.table = [[] for i in range(self.depth)]

        # a list to store all distinct values if F0 < t
        self.naive_lst = set()

    def _binary_search(self, a, x):
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        else:
            return -1

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        if self.hash_type == "mmh3":
            return mmh3.hash128(token, seed, signed=False)/self.max_128_int

    def insert(self, token):
        """ Insert a token into the sketch. Token must be byte-like objects. """
        if len(self.naive_lst) < self.width:
            self.naive_lst.add(token)

        for i in range(self.depth):
            hash_value = self._hash(token, self.seeds[i])
            j = self._binary_search(self.table[i], hash_value)

            if j == -1:
                if len(self.table[i]) < self.width:
                    bisect.insort(self.table[i], hash_value)
                elif self.table[i][self.width-1] > hash_value:
                    bisect.insort(self.table[i], hash_value)
                    self.table[i].pop()

    def merge(self, S):
        """ Merge self and another sketch S that must have same seeds """
        # merge the small lists
        for x in S.naive_lst:
            if len(self.naive_lst) < self.width:
                self.naive_lst.add(x)
            else:
                break

        # merge the smallest hash values
        for i in range(self.depth):
            for x in S.table[i]:
                j = self._binary_search(self.table[i], x)
                if j  == -1:
                    if len(self.table[i]) < self.width:
                        bisect.insort(self.table[i], x)
                    elif self.table[i][self.width-1] > x:
                        bisect.insort(self.table[i], x)
                        self.table[i].pop()

    def estimator(self):
        """ Return the estimate for the number of distinct
        elements inserted so far """
        #start_time = time.time()
        if len(self.naive_lst) < self.width:
            result = len(self.naive_lst)
            return result
        est = [int(self.width/self.table[i][self.width-1]) for i in range(self.depth)]
        median_of_est = statistics.median(est)
        return int(median_of_est)
