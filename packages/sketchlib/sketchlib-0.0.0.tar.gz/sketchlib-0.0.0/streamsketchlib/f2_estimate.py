import mmh3
import statistics
import math

class F2Estimate():

    def __init__(self, epsilon=0.01, delta=0.01, c=3, hash_type="mmh3", seed=42):
        """ 
        estimate the second frequency moment of a stream using the tug-of-war sketch.
        epsilon: relative error, 
        delta: failure probability.
        """
        # initialize basic parameters
        self.epsilon = epsilon
        self.delta = delta
        self.hash_type = hash_type
        self.max_128_int = pow(2, 128)-1

        # store the basic sketch values in a table
        self.width = c * int(1/(self.epsilon*self.epsilon))
        self.depth = c * int(math.log(1/self.delta,2))
        self.table = [[0 for j in range(self.width)] for i in range(self.depth)]
        self.seeds = [[seed*i*j for j in range(self.width)] for i in range(self.depth)]

    def _hash(self, token, seed):
        """ 
        Compute the {-1,+1} hash of a token
        """
        if self.hash_type == "mmh3":
            x = mmh3.hash128(token, seed, signed=False)/self.max_128_int
            if x <= 0.5:
                return -1
            else:
                return 1
        else:
            return 0

    def insert(self, x, y):
        """
        Insert token x into the stream with weight y.
        """
        for i in range(self.depth):
            for j in range(self.width):
                self.table[i][j] += self._hash(x, self.seeds[i][j])*y

    def merge(self, S):
        """
        Merge with another F2 sketch S.
        Require that S has the same seed, eps, & delta.

        """
        for i in range(self.depth):
            for j in range(self.width):
                self.table[i][j] += S.table[i][j]

    def estimator(self):
        """
        Return the F2 estimator of the current stream.
        """
        avg = []
        for i in range(self.depth):
            row = [self.table[i][j]*self.table[i][j] for j in range(self.width)]
            avg.append(sum(row)/self.width)
        return statistics.median(avg)








