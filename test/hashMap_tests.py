import pytest
import random

from _cache import HashMap, get_random_string


def test_add_hashtable():
    hm = HashMap()

    key = get_random_string(100)
    value = random.randint(0, 10000000)
    hm.add(key, value)

    assert hm.get(key) == value


def test_add_same_keys():
    hm = HashMap()
    key, value = '1', 9999
    key1, value1 = '1', 9999
    hm.add(key, value)
    with pytest.raises(KeyError) as exc_info:
        print()
        hm.add(key1, value1)


def test_add_diff_keys():
    hm = HashMap()

    key, value = '1', 1
    key1, value1 = '2', 2
    hm.add(key, value)
    hm.add(key1, value1)
    assert key1 in hm
    assert key in hm


def test_try_add_same_keys():
    hm = HashMap()
    key, value = '1', 1
    key1, value1 = '1', 2
    hm.add(key, value)

    assert not hm.try_add(key1, value1)


def test_try_add_diff_keys():
    hm = HashMap()

    key, value = '1', 1
    key1, value1 = '2', 2
    hm.add(key, value)

    assert hm.try_add(key1, value1)


def test_key_in_hashmap():
    hm = HashMap()
    key, value = '1', 1
    key1, value1 = '2', 2
    hm.add(key, value)

    hm.add(key1, value1)

    assert key1 in hm
    assert key in hm
    assert 'PLACEHOLDER' not in hm


def test_delete_key():
    hm = HashMap()
    key, value = '1', 1
    key1, value1 = '2', 2
    hm.add(key, value)
    hm.add(key1, value1)
    hm.delete(key1)

    assert key1 not in hm


def test_big_data():
    hm = HashMap()
    key, value = '1', 777
    key1, value1 = '2', 888
    hm.add(key, value)
    hm.add(key1, value1)

    for _ in range(100000):
        hm.try_add(get_random_string(100), -1)


    assert key1 in hm
    assert key in hm


