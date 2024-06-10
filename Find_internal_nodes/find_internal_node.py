def find_internal_nodes_num(tree):
    # Create a set to store unique parent nodes
    internal_nodes = set()

    # Iterate through the tree list
    for parent in tree:
        if parent != -1:
            internal_nodes.add(parent)

    # The number of unique parent nodes is the number of internal nodes
    return len(internal_nodes)


my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))
