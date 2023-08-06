from abc import abstractmethod
from cm_hh_cash_register import HeavyHittersCMRegister


class AbstractHeavyHittersAlgorithm:
    @abstractmethod
    def insert(self, token, count):
        pass

    @abstractmethod
    def get_heavy_hitters(self):
        pass

    @abstractmethod
    def merge(self):
        pass


class HeavyHittersFinder:
    COUNTMIN=0
    MISRAGRIES=1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, algorithm=COUNTMIN):
        self.phi = 0.05
        self.epsilon = 0.2
        self.delta = 0.01

        if algorithm == HeavyHittersFinder.COUNTMIN:
            self._heavy_hitters_finder = HeavyHittersCMRegister
        elif algorithm ==HeavyHittersFinder.MISRAGRIES




