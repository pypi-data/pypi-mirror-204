import random

from streamsketchlib.count_min import CountMin
import pandas as pd
from pympler.asizeof import asizeof

def test_countmin():
    mincounter = CountMin()
    test = asizeof(mincounter)

    mincounter.insert('a', 10)
    mincounter.insert('b', 7)
    mincounter.insert('a', 3)
    mincounter.insert('d', 1)
    mincounter.insert('e', 7)
    mincounter.insert('c', 11)

    test = asizeof(mincounter)

    assert mincounter.estimate_count('a') >= 13
    assert mincounter.estimate_count('b') >= 7
    assert mincounter.estimate_count('c') >= 11
    assert mincounter.estimate_count('d') >= 1
    assert mincounter.estimate_count('e') >= 7


def test_merge():
    mincounter1 = CountMin()
    mincounter2 = CountMin.from_existing(mincounter1)

    mincounter1.insert('a', 10)
    mincounter1.insert('b', 7)
    mincounter1.insert('a', 3)
    mincounter1.insert('d', 1)
    mincounter1.insert('e', 7)
    mincounter1.insert('c', 11)

    mincounter2.insert('a', 5)
    mincounter2.insert('b', 9)
    mincounter2.insert('a', 6)
    mincounter2.insert('d', 14)
    mincounter2.insert('e', 10)
    mincounter2.insert('c', 13)

    mincounter1.merge(mincounter2)

    assert mincounter1.estimate_count('a') >= 24
    assert mincounter1.estimate_count('b') >= 16
    assert mincounter1.estimate_count('c') >= 24
    assert mincounter1.estimate_count('d') >= 15
    assert mincounter1.estimate_count('e') >= 17


def test_large_file():
    mincounter = CountMin()
    test = asizeof(mincounter)

    try:
        test_data = pd.read_csv('item_sales_filtered.csv')
        correct_quantities = pd.read_csv('correct_sums.csv')
    except FileNotFoundError as e:
        print('Test files not found. Skipping test.')
        return

    item_sales = test_data.values.tolist()
    true_sums = correct_quantities.values.tolist()
    counter = 0
    for item in item_sales:
        counter += 1
        mincounter.insert(str(item[0]), item[1])

    for i in range(10):
        item, true_sum = random.choice(true_sums)
        calculated_sum = mincounter.estimate_count(str(item))
        assert calculated_sum >= true_sum
