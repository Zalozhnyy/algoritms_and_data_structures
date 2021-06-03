import enum


class Direction(enum.Enum):
    ascending = 1
    descending = 2


class Node:
    def __init__(self, val):
        self.value: float = val
        self._next_pointer: Node = None

    def set_next(self, val):
        self._next_pointer = val

    def get_next(self):
        return self._next_pointer


class Stack:
    def __init__(self):
        self._end_pointer: Node = None

    def push(self, value: float):
        node = Node(value)
        if not self._end_pointer:
            self._end_pointer = node

        else:
            previous = self._end_pointer
            self._end_pointer = node
            self._end_pointer.set_next(previous)

    def pull(self):
        if not self._end_pointer:
            return None

        out = self._end_pointer.value
        self._end_pointer = self._end_pointer.get_next()

        return out

    def clear(self):
        self._end_pointer = None

    def copy(self):
        c = Stack()
        c._end_pointer = self._end_pointer
        return c


class Queue:
    def __init__(self):
        self._start_pointer: Node = None
        self._end_pointer: Node = None

    def push(self, value: float):
        node = Node(value)
        if not self._end_pointer:
            self._start_pointer = node
            self._end_pointer = node

        else:
            self._end_pointer.set_next(node)
            self._end_pointer = node

    def pull(self):
        if not self._start_pointer:
            return None

        out = self._start_pointer.value
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


class SortedLinkedList:
    def __init__(self, direction: Direction):
        # direction  по убыванию и возрастанию
        self._direction = direction
        self._first_pointer: Node = None

    # def insert(self, value: float):
    #     new_node = Node(value)
    #     new_node.set_next(self._first_pointer)
    #     self._first_pointer = new_node

    def insert(self, value: float):
        if self._direction == Direction.ascending:
            self.ascending_case(value)
        elif self._direction == Direction.descending:
            self.descending_case(value)

    def ascending_case(self, value: float):
        # case empty list

        if not self._first_pointer:
            self._first_pointer = Node(value)

        elif self._first_pointer.value >= value:
            s = self._first_pointer
            self._first_pointer = Node(value)
            self._first_pointer.set_next(s)

        else:

            current = self._first_pointer

            while current.get_next() is not None and current.get_next().value < value:
                current = current.get_next()
            next = current.get_next()
            current.set_next(Node(value))
            current.get_next().set_next(next)

    def descending_case(self, value: float):
        # case empty list
        if not self._first_pointer:
            self._first_pointer = Node(value)

        elif self._first_pointer.value <= value:
            s = self._first_pointer
            self._first_pointer = Node(value)
            self._first_pointer.set_next(s)

        else:
            current = self._first_pointer

            while current.get_next() is not None and current.get_next().value > value:
                current = current.get_next()
            next = current.get_next()
            current.set_next(Node(value))
            current.get_next().set_next(next)

    def print_ll(self):

        cur = self._first_pointer
        while True:
            print(cur.value)
            cur = cur.get_next()
            if not cur:
                break

    def get_direction(self):
        return self._direction

    def reverse(self):

        previous = None
        current = self._first_pointer
        next = current.get_next()

        while next:
            current.set_next(previous)
            previous = current
            current = next
            next = current.get_next()

        current.set_next(previous)
        self._first_pointer = current

        self._direction = Direction.descending if self._direction == Direction.ascending else Direction.ascending


if __name__ == '__main__':
    # d = (1, 58, 25, 9, 85, 54, 895, 5, 5, 56, 78, 45, 2, 48, 89, 456, 15, 8, 78945)
    # d = (1, 58, 25, 9, 85)
    d = (1, 2, 3, 4, 5)

    ll = SortedLinkedList(Direction.ascending)
    # ll = SortedLinkedList(Direction.descending)

    for i in d:
        ll.insert(i)
    ll.print_ll()
    ll.insert(98)
    ll.reverse()
    print('========================')
    ll.print_ll()
    ll.insert(104)
    print('========================')
    ll.print_ll()
