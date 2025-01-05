from dataclasses import dataclass
from enum import Enum, auto


class BST:
    @dataclass
    class BSTNode:
        left: "BST.BSTNode" | None = None
        right: "BST.BSTNode" | None = None
        value: int

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
            self.root = val
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
                cur_node = cur_node.rigth
                from_left = False
        if from_left:
            prev_node.left = new_node
        else:
            prev_node.right = new_node

    def find_val(self, val):
        cur_node = self.root
        while cur_node.val != val:
            if cur_node is None:
                return False
            if cur_node.val > val:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        return True

    def remove_element(self, val):
        pass

    def __iter__(self):
        yield from self._in_order()

    def __len__(self):
        n_nodes = 0
        for _ in self._in_order:
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
