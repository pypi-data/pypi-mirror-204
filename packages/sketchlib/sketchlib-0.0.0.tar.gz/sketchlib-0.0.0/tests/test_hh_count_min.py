from streamsketchlib.cm_hh_cash_register import HeavyHittersCMRegister

import pandas as pd
from pympler.asizeof import asizeof
from time import time


def test_bidict_small():
    test_hh_cm = HeavyHittersCMRegister(phi=0.01, epsilon=0.2)
    test = asizeof(test_hh_cm)

    test_hh_cm.insert("This", 1)
    test_hh_cm.insert("is", 1)
    test_hh_cm.insert("is", 3)
    test_hh_cm.insert("only", 1)
    test_hh_cm.insert("a", 1)
    test_hh_cm.insert("a", 2)
    test_hh_cm.insert("test.", 10000)
    test_hh_cm.insert("b", 1)
    test_hh_cm.insert("c", 1)
    test_hh_cm.insert("d", 1)

    test = asizeof(test_hh_cm)

    test = test_hh_cm.get_heavy_hitters()
    assert test == ['test.']


def test_bidict_large():
    test_hh_cm = HeavyHittersCMRegister(phi=0.005, epsilon=0.2)
    test_hh_dict = dict()

    test_cm_size_start = asizeof(test_hh_cm)
    test_dict_size_start = asizeof(test_hh_dict)

    try:
        test_data = pd.read_csv('item_sales_filtered.csv')

    except FileNotFoundError as e:
        print('Test files not found. Skipping test.')
        return

    item_sales = test_data.values.tolist()

    start_dict = time()
    for item in item_sales:
        if item[0] in test_hh_dict:
            test_hh_dict[item[0]] += item[1]
        else:
            test_hh_dict[item[0]] = item[1]
    end_dict = time()

    dict_time = end_dict - start_dict
    test_dict_size_end = asizeof(test_hh_dict)

    start_cm = time()
    for item in item_sales:
        test_hh_cm.insert(str(item[0]), item[1])
    end_cm = time()

    cm_time = end_cm - start_cm
    test_cm_size_end = asizeof(test_hh_cm)

    test = test_hh_cm.get_heavy_hitters()
    assert '1503844' in test
    assert '1473474' in test
    assert '2042941' in test
    assert '2042947' in test
    assert '819932' not in test


def test_bidict_kindle():
    test_hh_cm = HeavyHittersCMRegister(phi=0.01, epsilon=0.2)
    test_hh_dict = dict()

    test_cm_size_start = asizeof(test_hh_cm)
    test_dict_size_start = asizeof(test_hh_dict)

    try:
        test_data = pd.read_csv('kindle_reviews.csv')

    except FileNotFoundError as e:
        print('Test files not found. Skipping test.')
        return

    test_data = test_data['reviewerName']
    reviewers = test_data.tolist()

    start_dict = time()
    for reviewer in reviewers:
        if reviewer in test_hh_dict:
            test_hh_dict[reviewer] += 1
        else:
            test_hh_dict[reviewer] = 1
    end_dict = time()

    dict_time = end_dict - start_dict
    test_dict_size_end = asizeof(test_hh_dict)

    start_cm = time()
    for reviewer in reviewers:
        test_hh_cm.insert(str(reviewer), 1)
    end_cm = time()
    cm_time = end_cm - start_cm

    test_cm_size_end = asizeof(test_hh_cm)

    test_hh = test_hh_cm.get_heavy_hitters()
    assert 'Amazon Customer' in test_hh
    assert 'Kindle Customer' in test_hh


def test_small_merge():
    test_hh_cm = HeavyHittersCMRegister(phi=0.01, epsilon=0.2)
    test_hh_cm_2 = HeavyHittersCMRegister.from_existing(test_hh_cm)

    test_hh_cm.insert("This", 1)
    test_hh_cm.insert("is", 1)
    test_hh_cm.insert("is", 3)
    test_hh_cm.insert("only", 1)
    test_hh_cm.insert("a", 1)
    test_hh_cm.insert("a", 2)
    test_hh_cm.insert("test.", 10000)
    test_hh_cm.insert("b", 1)
    test_hh_cm.insert("c", 1)
    test_hh_cm.insert("d", 1)

    test_hh_cm_2.insert("This", 1)
    test_hh_cm_2.insert("is", 400)
    test_hh_cm_2.insert("is", 3)
    test_hh_cm_2.insert("only", 90)
    test_hh_cm_2.insert("a", 1)
    test_hh_cm_2.insert("a", 2)
    test_hh_cm_2.insert("test.", 1)
    test_hh_cm_2.insert("b", 1)
    test_hh_cm_2.insert("c", 1)
    test_hh_cm_2.insert("d", 1)

    test1 = test_hh_cm.get_heavy_hitters()
    test2 = test_hh_cm_2.get_heavy_hitters()

    assert 'test.' in test1
    assert 'is' in test2
    assert 'only' in test2

    test_hh_cm.merge(test_hh_cm_2)
    merge_test = test_hh_cm.get_heavy_hitters()

    assert 'test.' in merge_test
    assert 'is' in merge_test
    assert 'only' not in merge_test
