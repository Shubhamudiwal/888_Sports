def find_internal_nodes_num(tree):
    # Step 1: Create a list to store the number of children for each node
    num_nodes = len(tree)
    children_count = [0] * num_nodes

    # Step 2: Populate the children count list
    for parent in tree:
        if parent != -1:
            children_count[parent] += 1

    # Step 3: Count nodes with at least one child (internal nodes)
    internal_nodes_count = sum(1 for count in children_count if count > 0)

    return internal_nodes_count


# Test the function with the provided tree
my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))  # Output should be 3
