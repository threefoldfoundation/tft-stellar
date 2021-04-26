# PORTED FROM OLD Rivine JS960 code,
# perhaps we can remove this file in the future,
# or at the very least it should probably be(come/replaced-by) a global JS solution.

# // A Tree takes data as leaves and returns the Merkle root. Each call to 'Push'
# // adds one leaf to the Merkle tree. Calling 'Root' returns the Merkle root.
# // The Tree also constructs proof that a single leaf is a part of the tree. The
# // leaf can be chosen with 'SetIndex'. The memory footprint of Tree grows in
# // O(log(n)) in the number of leaves.
class Tree:
    """
    // The Tree is stored as a stack of subtrees. Each subtree has a height,
	// and is the Merkle root of 2^height leaves. A Tree with 11 nodes is
	// represented as a subtree of height 3 (8 nodes), a subtree of height 1 (2
	// nodes), and a subtree of height 0 (1 node). Head points to the smallest
	// tree. When a new leaf is inserted, it is inserted as a subtree of height
	// 0. If there is another subtree of the same height, both can be removed,
	// combined, and then inserted as a subtree of height n + 1.
    """

    def __init__(self, hash_func):
        self.head = None
        self.hash_func = hash_func

    def push(self, data):
        """
        // Push will add data to the set, building out the Merkle tree and Root. The
        // tree does not remember all elements that are added, instead only keeping the
        // log(n) elements that are necessary to build the Merkle root and keeping the
        // log(n) elements necessary to build a proof that a piece of data is in the
        // Merkle tree.
        """

        # // Hash the data to create a subtree of height 0. The sum of the new node
        # // is going to be the data for cached trees, and is going to be the result
        # // of calling leafSum() on the data for standard trees. Doing a check here
        # // prevents needing to duplicate the entire 'Push' function for the trees.
        self.head = SubTree(next=self.head, height=0)

        self.head.sum = leaf_sum(self.hash_func, data)

        # // Insert the subTree into the Tree. As long as the height of the next
        # // subTree is the same as the height of the current subTree, the two will
        # // be combined into a single subTree of height n+1.
        while self.head.next is not None and self.head.height == self.head.next.height:
            # // Join the two subTrees into one subTree with a greater height. Then
            # // compare the new subTree to the next subTree.
            self.head = join_subtree(self.hash_func, self.head.next, self.head)

    def root(self):
        """
        // Root returns the Merkle root of the data that has been pushed.
        """
        if self.head is None:
            return sum(self.hash_func, bytearray())

        # // The root is formed by hashing together subTrees in order from least in
        # // height to greatest in height. The taller subtree is the first subtree in
        # // the join.
        current = self.head
        while current.next is not None:
            current = join_subtree(self.hash_func, current.next, current)
        return current.sum


class SubTree:
    """
    // A subTree contains the Merkle root of a complete (2^height leaves) subTree
    // of the Tree. 'sum' is the Merkle root of the subTree. If 'next' is not nil,
    // it will be a tree with a higher height.
    """

    def __init__(self, next, height):
        self.next = next
        self.height = height
        self.sum = bytearray()


def sum_(hash_func, data):
    """
    // sum returns the hash of the input data using the specified algorithm.
    """
    if data is None:
        return None
    result = hash_func(data)
    if hasattr(result, "digest"):
        result = result.digest()
    # print("Data is: {} Result is: {}".format(data.hex(), result.hex()))
    return result


def leaf_sum(hash_func, data):
    """
    // leafSum returns the hash created from data inserted to form a leaf. Leaf
    // sums are calculated using:
    //		Hash( 0x00 || data)
    """
    # print("Calling leafSum")
    data_ = bytearray([0])
    data_.extend(data)
    return sum_(hash_func, data_)


def node_sum(hash_func, a, b):
    """
    // nodeSum returns the hash created from two sibling nodes being combined into
    // a parent node. Node sums are calculated using:
    //		Hash( 0x01 || left sibling sum || right sibling sum)
    """
    # print("Calling node_sum")
    data_ = bytearray([1])
    data_.extend(a)
    data_.extend(b)
    return sum_(hash_func, data_)


def join_subtree(hash_func, a, b):
    """
    // joinSubTrees combines two equal sized subTrees into a larger subTree.
    """
    # print('Calling joinSubtree')
    stree = SubTree(next=a.next, height=a.height + 1)
    stree.sum = node_sum(hash_func, a.sum, b.sum)
    return stree


if __name__ == "__main__":
    from Jumpscale import j

    tree = Tree(hash_func=lambda o: bytes.fromhex(j.data.hash.blake2_string(o)))
    tree.push(bytearray([1]))
    tree.push(bytearray([2]))
    tree.push(bytearray([3]))
    tree.push(bytearray([4]))
    tree.push(bytearray([5]))
    root = tree.root().hex()
    assert root == "0002789a97a9feee38af3709f06377ef0ad7d91407cbcad1ccb8605556b6578e"
    print("Root is {}".format(root))
