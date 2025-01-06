from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class BST:
    @dataclass
    class BSTNode:
        value: int
        left: Union["BST.BSTNode", None] = None
        right: Union["BST.BSTNode", None] = None

    class IterType(Enum):
        pre_order = auto()
        in_order = auto()
        post_order = auto()

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def insert_element(self, val):
        new_node = BST.BSTNode(val)
        if self.root is None:
            self.root = new_node
            return
        cur_node = self.root
        prev_node = cur_node
        from_left = True
        while not cur_node is None:
            prev_node = cur_node
            if cur_node.value > val:
                cur_node = cur_node.left
                from_left = True
            else:
                cur_node = cur_node.right
                from_left = False
        if from_left:
            prev_node.left = new_node
        else:
            prev_node.right = new_node

    def find_val(self, val) -> bool:
        cur_node = self.root
        while cur_node.value != val:
            if cur_node is None:
                return False
            if cur_node.value > val:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        return True

    def remove_element(self, val) -> bool:
        self._remove_node(self.root, val)
        return True

    def _remove_node(self, node: BSTNode, val):
        # search recursively node with requested value
        if node is None:
            return None

        if node.value > val:
            node.left = self._remove_node(node.left, val)
        elif node.value < val:
            node.right = self._remove_node(node.right, val)

        else:  # value found, remove node
            # leaf case
            if node.left is None and node.right is None:
                return None
            # one child
            if not node.left or not node.right:
                return node.left or node.right

            # two children
            # find next
            next_node = self._in_order(node)
            node.value = next_node.value
            node.right = self._remove_node(node.right, next_node.value)
        return node

    def __iter__(self):
        yield from self._in_order()

    def __len__(self):
        n_nodes = 0
        for _ in self._in_order(self.root):
            n_nodes += 1
        return n_nodes

    def _in_order(self, root: BSTNode):
        if root:
            yield from self._in_order(root.left)
            yield root.value
            yield from self._in_order(root.right)

    def _pre_order(self, root: BSTNode):
        if root:
            yield root.value
            yield from self._pre_order(root.left)
            yield from self._pre_order(root.right)

    def _post_order(self, root: BSTNode):
        if root:
            yield from self._post_order(root.left)
            yield from self._post_order(root.right)
            yield root.value


if __name__ == "__main__":
    # generate tree tests
    # test insert
    def test_insert():
        bst = BST()
        for i in range(10):
            bst.insert_element(i)
        assert len(bst) == 10
        print("Test insert passed")

    # test remove
    def test_remove():
        bst = BST()
        for i in range(10):
            bst.insert_element(i)
        bst.remove_element(5)
        assert len(bst) == 9
        print("Test remove passed")

    # test find
    def test_find():
        bst = BST()
        for i in range(10):
            bst.insert_element(i)
        assert bst.find_val(5)
        print("Test find passed")

    test_insert()
    test_remove()
    test_find()
