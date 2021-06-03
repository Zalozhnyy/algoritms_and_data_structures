from __future__ import annotations


class Node:  # fix bin tree
    def __init__(self, val: float):
        self.value: float = val
        self._left: Node = None
        self._right: Node = None

    def set_child(self, child: Node):
        if child.value < self.value:
            assert self._left is None
            self._left = child
        else:
            assert self._right is None
            self._right = child

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right


class SearchBinaryTree:  # binary search tree !!!NO RECURSION!!!
    def __init__(self):
        self._head: Node = None

    def insert(self, value: float):
        current = self._head
        if not self._head:
            self._head = Node(value)

        elif self._head.value < value:  # left case
            self._head.set_child(Node(value))


    def print(self):  # по ворастанию
        pass


if __name__ == '__main__':
    d = (1, 2, 3, 4, 5)

    bt = SearchBinaryTree()
    for i in d:
        bt.insert(i)
