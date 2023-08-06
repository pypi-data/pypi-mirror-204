import random


class RsvSampling:
    """
    Sample a random element in a data stream without knowing the stream length
    """
    def __init__(self, rsv_size):
        """ Return k random tokens (without replacement) from the stream
        """
        self.rsv = []
        self.rsv_size = rsv_size
        self.stream_length = 0

    def insert(self, token):
        """ Insert a token into the stream. """
        self.stream_length += 1
        if len(self.rsv) < self.rsv_size:
            self.rsv.append(token)
        else:
            j = random.randint(1, self.stream_length)
            if j <= self.rsv_size:
                self.rsv[j-1] = token

    def reservoir(self):
        """ Return the list of sampled tokens """
        return self.rsv