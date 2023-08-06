from streamsketchlib.count_min import CountMin
from heapq import heappush, heappop, heapify


class HeavyHittersCMRegister:
    """ This class solves the heavy hitters problem using a count-min data
        structure. It works only for the cash register model of a stream where
        each token count must be greater than 0 (c > 0)."""
    def __init__(self, phi=0.01, epsilon=0.1, delta=0.01):
        self.phi = phi
        self.epsilon = epsilon
        self.delta = delta
        self.count_min = CountMin(phi=self.phi, epsilon=self.epsilon,
                                  delta=self.delta, seed=pow(13, 2))
        self.l1_norm = 0
        self._min_heap = []

    def insert(self, token, count):
        self.l1_norm += count
        cutoff = self.phi * self.l1_norm

        self.count_min.insert(str(token), count)
        point_query = self.count_min.estimate_count(token)
        if point_query >= cutoff:
            heappush(self._min_heap, (point_query, token))

        if len(self._min_heap) > 0:
            smallest_estimate = self._min_heap[0][0]
            while smallest_estimate < cutoff and len(self._min_heap) > 0:
                heappop(self._min_heap)
                if len(self._min_heap) > 0:
                    smallest_estimate = self._min_heap[0][0]

    def get_heavy_hitters(self):
        heavy_hitters = set()
        for count, item in self._min_heap:
            if item not in heavy_hitters:
                heavy_hitters.add(item)
        return list(heavy_hitters)

    @classmethod
    def from_existing(cls, original):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm_hh = cls()
        new_cm_hh.epsilon = original.epsilon
        new_cm_hh.delta = original.delta
        new_cm_hh.phi = original.phi
        new_cm_hh.count_min = CountMin.from_existing(original.count_min)
        new_cm_hh.l1_norm = 0
        new_cm_hh._min_heap = []
        return new_cm_hh

    def merge(self, other_instance):
        """ Merges other heavy-hitter instance into self. Both instance being
            merged and the instance being merged into need to share all
            parameters and hash seeds. Otherwise, the merge will fail. If it
            does not fail, the results will be meaningless. """
        self.count_min.merge(other_instance.count_min)

        self.l1_norm += other_instance.l1_norm
        cutoff = self.l1_norm * self.phi

        # A heavy-hitter in merged instance must have been heavy hitter in
        # at least one instance prior to merge.
        self._min_heap.extend(other_instance._min_heap)
        heapify(self._min_heap)

        # Remove any tokens that are no longer heavy hitters.
        smallest_estimate = self._min_heap[0][0]
        while smallest_estimate < cutoff and len(self._min_heap) > 0:
            old_value, token = heappop(self._min_heap)
            # Check to see if new token count qualifies it as a heavy hitter
            new_estimate = self.count_min.estimate_count(token)
            if new_estimate >= cutoff:
                heappush(self._min_heap, (new_estimate, token))
            if len(self._min_heap) > 0:
                smallest_estimate = self._min_heap[0][0]
