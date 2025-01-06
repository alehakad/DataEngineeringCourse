class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def pruneTree(root: TreeNode):
    # post order traversal
    if root is None:
        return None

    root.left = pruneTree(root.left)
    root.right = pruneTree(root.right)

    if root.value == 0 and root.left is None and root.right is None:
        return None

    return root


if __name__ == "__main__":
    leaf_left = TreeNode(0)
    leaf_right = TreeNode(0)
    leaf_parent = TreeNode(1, leaf_left, leaf_right)
    leaf_left_left = TreeNode(0)
    leaf_parent_parent = TreeNode(0, leaf_parent, leaf_left_left)
    leaf_rigth_right = TreeNode(1)
    root = TreeNode(0, leaf_parent_parent)

    pruneTree(root)
