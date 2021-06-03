from __future__ import annotations


class Node:  # fix bin tree
    def __init__(self, val: float):
        self.value: float = val
        self._left: Node = None
        self._right: Node = None

    def set_left(self, child: Node):
        assert self._left is None
        self._left = child

    def set_right(self, child: Node):
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
        inserted_node = Node(value)
        current = self._head

        if not self._head:
            self._head = inserted_node

        else:

            while current:
                if value < current.value:
                    if not current.get_left():
                        current.set_left(inserted_node)
                        break
                    else:
                        current = current.get_left()
                else:
                    if not current.get_right():
                        current.set_right(inserted_node)
                        break
                    else:
                        current = current.get_right()

    def print(self):  # по ворастанию
        pass

    def print_width(self):

        current = self._head
        level = []
        if current.get_left():
            level.append(current.get_left())
        if current.get_right():
            level.append(current.get_right())
        next_level = []
        print(current.value)

        while True:
            tmp = ''
            for node in level:
                tmp += str(node.value) + '-'
                if node.get_left():
                    next_level.append(node.get_left())
                if node.get_right():
                    next_level.append(node.get_right())

            print(tmp)
            if len(next_level) == 0:
                break

            level = [i for i in next_level]
            next_level = []


if __name__ == '__main__':
    d = (5, 2, 3, 4, 5, 8, 10, 134)

    bt = SearchBinaryTree()
    for i in d:
        bt.insert(i)

    bt.print_width()
