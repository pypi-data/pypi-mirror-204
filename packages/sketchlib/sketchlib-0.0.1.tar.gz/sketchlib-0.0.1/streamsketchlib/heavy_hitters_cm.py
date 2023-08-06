from math import ceil, log2
from bidict import bidict
from streamsketchlib.count_min import CountMin
from collections import deque


class HeavyHittersCM:

    def __init__(self, n=100000, phi=0.01, epsilon=0.2, delta=0.05):
        self.n = n
        self.phi = phi
        self.epsilon = epsilon
        self.delta = delta

        self.cm_rows = ceil(log2(self.n)) + 1
        self.count_min_array = [CountMin(phi=self.phi,
                                         epsilon=self.epsilon,
                                         delta=self.delta,
                                         seed=pow(i+13, 2))
                                for i in range(self.cm_rows)]
        self.l1_norm = 0
        self.token_dict = bidict()
        self._token_label = 0

    def insert(self, token, count):
        self.l1_norm += count

        if token not in self.token_dict:
            self.token_dict[token] = self._token_label
            self._token_label += 1

        token_label = self.token_dict[token]
        for i in range(self.cm_rows):
            divisor = pow(2, self.cm_rows-i-1)
            interval = int(token_label/divisor)
            self.count_min_array[i].insert(str(interval), count)

    def get_heavy_hitters(self):
        queue = deque()
        queue.append([0, 0])
        cutoff = self.l1_norm * self.phi
        heavy_hitters = []

        while len(queue) > 0:
            row, interval = queue.popleft()
            estimate = self.count_min_array[row].get_frequency(str(interval))
            if estimate >= cutoff:
                if row < self.cm_rows-1:
                    queue.append([row + 1, 2 * interval])
                    queue.append([row + 1, 2 * interval + 1])
                else:
                    heavy_token = self.token_dict.inverse[interval]
                    heavy_hitters.append(heavy_token)
        return heavy_hitters
