import string
import random


class HashNode:
    def __init__(self, key: str = None, value: float = None):
        self.value = value
        self.key = key
        self._next_pointer: HashNode = None

    def set_next(self, val):
        self._next_pointer = val

    def get_next(self):
        return self._next_pointer


class Queue:
    def __init__(self):
        self._start_pointer: HashNode = None
        self._end_pointer: HashNode = None

    def push(self, key: str, value: float):
        node = HashNode(key, value)
        if not self._end_pointer:
            self._start_pointer = node
            self._end_pointer = node

        else:
            self._end_pointer.set_next(node)
            self._end_pointer = node

    def pull(self):
        if not self._start_pointer:
            return None

        out = self._start_pointer
        self._start_pointer = self._start_pointer.get_next()

        if self._start_pointer is None:
            self._end_pointer = None

        return out

    def peek(self):
        if not self._start_pointer:
            return None
        return self._start_pointer.value

    def clear(self):
        self._start_pointer = None
        self._end_pointer = None

    def is_empty(self):
        if self._start_pointer is None and self._end_pointer is None:
            return True
        else:
            return False


class HashLinkedList:
    def __init__(self):
        self._first_pointer: HashNode = None
        self.len = 0

        self.__iteration_pointer: HashNode = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__iteration_pointer:
            self.__iteration_pointer = self._first_pointer
            if not self.__iteration_pointer:
                raise StopIteration
            return self.__iteration_pointer

        if self.__iteration_pointer.get_next():
            self.__iteration_pointer = self.__iteration_pointer.get_next()
            return self.__iteration_pointer
        else:
            raise StopIteration

    def __contains__(self, key: str):
        found = False

        current = self._first_pointer
        while current:
            if current.key == key:
                found = True
                break

            current = current.get_next()
            if not current:
                break
        return found

    def insert(self, key: str, value: float):
        new_node = HashNode(key, value)
        new_node.set_next(self._first_pointer)
        self._first_pointer = new_node
        self.len += 1

    def delete(self, key):
        current = self._first_pointer
        previous = None
        while current:

            if current.key == key:
                if not previous:
                    self._first_pointer = current.get_next()
                else:
                    previous.set_next(current.get_next())
                self.len -= 1
                return
            previous = current
            current = current.get_next()

        print(f'key {key} not exist')

    def find(self, key: str) -> float:
        found = None
        current = self._first_pointer
        if current.key == key:
            return current.value
        while current.get_next():
            if current.key == key:
                found = current
                break
        return found.value

    def print_ll(self):

        cur = self._first_pointer
        if not cur:
            print('empty')
            return
        while True:
            print(cur.value)
            cur = cur.get_next()
            if not cur:
                break


class HashMap:
    # hm = HashMap()
    #
    # hm.add('one', 1)
    # hm.add('two', 2)
    # hm.add('three', 3)
    # hm.add('four', 4)
    #
    # hm.delete('four')
    #
    # for _ in range(100):
    #     hm.add(get_random_string(10), random.randint(-1000, 1000))
    #
    # hm._print_hash_tables()

    def __init__(self):
        self._size = 2

        self._max_length = 10

        self._table: list[HashLinkedList] = [HashLinkedList() for _ in range(self._size)]

    def __contains__(self, key):
        table_index = hash(key) % self._size
        return key in self._table[table_index]

    def try_add(self, key: str, value: float) -> bool:
        table_index = hash(key) % self._size
        if key not in self._table[table_index]:
            self._table[table_index].insert(key, value)
        else:
            return False

        if self._table[table_index].len > self._max_length:
            self._rehash_table()

        return True

    def add(self, key: str, value: float):
        table_index = hash(key) % self._size
        if key not in self._table[table_index]:
            self._table[table_index].insert(key, value)
        else:
            raise KeyError(f'key:{key} already in linkedList')
        if self._table[table_index].len > self._max_length:
            self._rehash_table()

    def get(self, key: str):
        table_index = hash(key) % self._size
        return self._table[table_index].find(key)

    def _print_hash_tables(self):
        for i in range(self._size):
            print(f'Table index {i}')
            self._table[i].print_ll()

    def delete(self, key: str):
        table_index = hash(key) % self._size
        self._table[table_index].delete(key)

    def _rehash_table(self):
        self._size *= 2

        old_table = [i for i in self._table]
        self._table = [HashLinkedList() for _ in range(self._size)]

        for i in range(len(old_table)):
            for node in old_table[i]:
                key, value = node.key, node.value
                self.add(key, value)


class Cache:
    def __init__(self, max_elements=2):
        self._max = max_elements
        self._elements_counter = 0

        self._cache: HashMap = HashMap()

    def __contains__(self, key: str):
        return key in self._cache

    def add(self, key: str, value: float) -> bool:
        self._cache.add(key, value)
        self._elements_counter += 1

        if self._elements_counter > self._max:
            return True

        return False

    def delete(self, key: str):
        self._cache.delete(key)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == '__main__':
    c = Cache(max_elements=40)
    q = Queue()

    for i in range(4000):
        key, value = get_random_string(10), i
        q.push(key, value)
        if c.add(key, value):
            delete_object = q.pull()
            c.delete(delete_object.key)

    c._cache._print_hash_tables()
