import pytest

from _cache import Cache, Queue


def test_values_not_in_cache():
    N = 4000
    elements = 40

    c = Cache(max_elements=elements)
    q = Queue()

    for i in range(N):
        key, value = f'{i}', i
        q.push(key, value)
        if c.add(key, value):
            delete_object = q.pull()
            c.delete(delete_object.key)

    for i in range(N - elements):
        assert str(i) not in c


def test_values_in_cache():
    N = 4000
    elements = 40

    c = Cache(max_elements=elements)
    q = Queue()

    for i in range(N):
        key, value = f'{i}', i
        q.push(key, value)
        if c.add(key, value):
            delete_object = q.pull()
            c.delete(delete_object.key)

    for i in range(N - elements, N):
        assert str(i) in c
