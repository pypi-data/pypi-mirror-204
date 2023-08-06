from math import ceil
from sys import getsizeof


class MisraGries:
    """ Implements the Misra-Gries algorithm for finding frequent items (ie
        heavy hitters). """

    def __init__(self, k=100):
        """ Parameter k controls heavy hitter threshold, i.e., total_count/k
            k - number of buckets
            m - count of all elements encountered (length of stream)
            phi - heavy hitters are elements occurring >= (phi * m) times
            epsilon - margin of error - elements occurring > (1-eps)*phi*m
                    times may be returned
        """
        self.k = k
        self.epsilon = 0.2
        self.phi = 1 / (self.k * self.epsilon)
        self.counters = {}
        self.m = 0

    @classmethod
    def from_phi_and_eps(cls, phi=0.0025, epsilon=0.2):
        """ Initializes Misra-Gries instance directly from phi and epsilon."""
        new_misra = cls()
        new_misra.phi = phi
        new_misra.epsilon = epsilon
        new_misra.k = ceil(1 / (phi * epsilon))
        return new_misra

    def insert(self, token):
        """ Processes a new token into the dictionary. If an element already
            occupies a bucket, then increment that bucket count. If not, then
            if there are available buckets, store the token in a new bucket.
            Otherwise, decrement the count of all other buckets.
            Input: token - could be string or number """
        self.m += 1
        if token in self.counters:
            self.counters[token] += 1
        else:
            if len(self.counters) < self.k-1:
                self.counters[token] = 1
            else:
                for y in list(self.counters):
                    self.counters[y] -= 1
                    if self.counters[y] == 0:
                        del self.counters[y]

    def top_counters(self, amount):
        """ Return the buckets of top estimate counts
        count - stream length/num_buckets <= estimate count <= count
        """
        sorted_freq = sorted(self.counters, key=self.counters.get,
                             reverse=True)
        sorted_counters = {}
        for y in sorted_freq[:amount]:
            sorted_counters[y] = self.counters[y]
        return sorted_counters

    def get_heavy_hitters(self):
        """ Elements that occur more than phi * m times in stream are heavy
            hitters will be returned. Those occurring less than (1-eps)*phi*m
            times will be ignored. Those within the margin may or may not be
            returned """
        heavy_hitters = {}
        counters = self.counters.copy()
        threshold = (1 - self.epsilon) * self.phi * self.m
        for key, counter in counters.items():
            if counter > threshold:
                heavy_hitters[key] = self.counters[key]
        return heavy_hitters

    def merge(self, other_sketch):
        """ Merge with another Misra-Gries sketch
        Requirements: other sketch must have the same number of counters k
        """
        self.m += other_sketch.m
        # adding counts key-wise
        for x in other_sketch.counters:
            if x in self.counters:
                self.counters[x] += other_sketch.counters[x]
            else:
                self.counters[x] = other_sketch.counters[x]
        # Remove (k+1)th counter value from the remaining counters
        keys_to_delete = []
        if len(self.counters) > self.k:
            sorted_values = sorted(self.counters.values(), reverse=True)
            c = sorted_values[self.k]
            for key in self.counters.keys():
                self.counters[key] -= c
                if self.counters[key] <= 0:
                    keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.counters[key]

    def get_memory_footprint(self):
        size = 0
        size += getsizeof(self)
        size += getsizeof(self.k)
        size += getsizeof(self.m)
        size += getsizeof(self.epsilon)
        size += getsizeof(self.phi)
        size += getsizeof(self.counters)
        for key, value in self.counters.items():
            size += getsizeof(key)
            size += getsizeof(value)
        return size
