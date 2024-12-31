from typing import Optional


class Node:
    def __init__(self, value: int, next: Optional["Node"] = None):
        self.value = value
        self.next = next

    def add_next(self, next: "Node"):
        self.next = next

    def get_value(self):
        return self.value


class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self.n_nodes = 0

    def push(self, value: int):
        new_node = Node(value=value)
        if self._tail is not None:
            self._tail.add_next(new_node)
            self._tail = new_node
        else:
            self._tail = new_node
            self._head = new_node
        self.n_nodes += 1

    def pop(self):
        self._head = self._head.next
        self.n_nodes -= 1

    def head(self) -> int:
        return self._head.get_value()

    def __len__(self) -> int:
        return self.n_nodes

    def is_empty(self) -> bool:
        return self._head is None


if __name__ == "__main__":

    def test_linked_list():
        # Create an empty linked list
        linked_list = LinkedList()
        assert len(linked_list) == 0
        assert linked_list.is_empty() is True

        # Push elements into the linked list
        linked_list.push(10)
        linked_list.push(20)
        linked_list.push(30)
        assert len(linked_list) == 3
        assert linked_list.is_empty() is False

        # Check the head value
        assert linked_list.head() == 10

        # Pop an element from the linked list
        linked_list.pop()
        assert len(linked_list) == 2

        # Push another element
        linked_list.push(40)
        assert len(linked_list) == 3

        # Check the head value again
        assert linked_list.head() == 20

        # Pop all elements from the linked list
        linked_list.pop()
        linked_list.pop()
        linked_list.pop()
        assert len(linked_list) == 0
        assert linked_list.is_empty() is True

    test_linked_list()
