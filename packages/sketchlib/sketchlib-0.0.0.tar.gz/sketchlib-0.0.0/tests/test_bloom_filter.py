from streamsketchlib.bloom_filter import BloomFilter


from streamsketchlib.bloom_filter import BloomFilter


def test_bloom_filter_1():
    test_n = 1000000

    test_bf = BloomFilter(n=test_n)

    for i in range(test_n):
        test_bf.insert(str(i))

    result = True
    for i in range(test_n):
        if not test_bf.membership(str(i)):
            result = False
    assert result

    false_positives = []

    for i in range(test_n, 2*test_n):
        if test_bf.membership(str(i)):
            false_positives.append(i)

    false_pos_count = len(false_positives)
    assert false_pos_count < (test_n * 0.012)


def test_bloom_filter_2():
    delta = 0.0001
    n = 100
    B = BloomFilter(n = n, delta = delta)
    for i in range(n):
        B.insert(str(i))
    
    result = True
    for i in range(n):
        if B.membership(str(i)) == False:
            result = False
    assert(result == True)

    false_positive = 0
    for i in range(n):
        if B.membership(str(i+n)) == True:
            false_positive += 1
    assert(false_positive <= 1.1*delta*n)


def test_bloom_filter_3():
    delta = 0.1
    n = 1000
    B = BloomFilter(n = n, delta = delta)
    for i in range(n):
        B.insert(str(i))
    
    result = True
    for i in range(n):
        if B.membership(str(i)) == False:
            result = False
    assert(result == True)

    false_positive = 0
    for i in range(n*n):
        if B.membership(str(i+2*n*n)) == True:
            false_positive += 1
    assert(false_positive <= 1.1*n*n*delta)


def test_bloom_filter_4():
    # insert 0,...,n-1 to B
    # insert n/2-1,...,3n/2-1 to C
    # merge 
    delta = 0.1
    n = 1000
    B = BloomFilter(n = 2*n, delta = delta)
    C = BloomFilter(n = 2*n, delta = delta)

    for i in range(n):
        B.insert(str(i))

    for i in range(int(n/2), int((3/2)*n)):
        C.insert(str(i))

    B.merge(C)
    
    result = True
    for i in range(int((3/2)*n)):
        if B.membership(str(i)) == False:
            result = False
    assert(result == True)

    false_positive = 0
    for i in range(2*n, 3*n):
        if B.membership(str(i)) == True:
            false_positive += 1
    assert(false_positive <= 1.1*n*delta)


def test_bloom_filter_5():
    # insert 0,...,n-1 to B
    # insert n/2-1,...,3n/2-1 to C
    # merge C to B
    # delete n,...,3n/2-1 from B
    delta = 0.1
    n = 1000
    B = BloomFilter(n = 2*n, delta = delta)
    C = BloomFilter(n = 2*n, delta = delta)
    result = True
    false_positive = 0

    for i in range(n):
        B.insert(str(i))

    for i in range(int(n/2), int((3/2)*n)):
        C.insert(str(i))

    B.merge(C)

    for i in range(n, int((3/2)*n)):
        B.delete(str(i))

    for i in range(n):
        if B.membership(str(i)) == False:
            result = False
    assert(result == True)

    for i in range(n, int((3/2)*n)):
        if B.membership(str(i)) == True:
            false_positive += 1
    assert(false_positive <= 1.1*delta*(1/2)*n)
    