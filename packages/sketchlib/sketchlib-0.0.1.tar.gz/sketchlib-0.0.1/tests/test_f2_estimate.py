from streamsketchlib.f2_estimate import F2Estimate

def test_f2():
    epsilon = 0.1
    delta = 0.01

    S = F2Estimate(epsilon = epsilon, delta = delta)

    S.insert('a', 10)
    S.insert('b', 5)
    S.insert('a', -2)
    S.insert('d', 1)
    S.insert('e', 30)
    S.insert('c', 20)
    S.insert('a', 40)
    S.insert('b', 25)

    test = S.estimator()
    assert test >= (1-epsilon)*4505 and test <= (1+epsilon)*4505

def test_f2_merge():
    epsilon = 0.1
    delta = 0.01

    S1 = F2Estimate(epsilon = epsilon, delta = delta)
    S2 = F2Estimate(epsilon = epsilon, delta = delta)

    S1.insert('a', 10)
    S1.insert('b', 5)
    S1.insert('a', -2)
    S1.insert('d', 1)
    S1.insert('e', 30)
    S1.insert('c', 20)
    S1.insert('a', 40)
    S1.insert('b', 25)

    S2.insert('a', 50)
    S2.insert('b', -5)
    S2.insert('a', -10)

    S1.merge(S2)
    test = S1.estimator()

    assert test >= (1-epsilon)*8326 and test <= (1+epsilon)*8326


if __name__ == '__main__':
    test_f2()
