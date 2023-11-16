

from ete3 import Tree

# no idea how to propagate lineno through nodes, so i have to make a custom map for it
line_numbers = {}


# [JT] lineno = number of line where the statement is declared
def make_node(node_name: str, children=None, lineno=-1) -> Tree:
    """
    It takes a node name and a list of children, and returns a tree

    :param node_name: The name of the node
    :type node_name: str
    :param children: A list of children to add to the node
    :return: A tree with the name of the node and the children
    """
    ast = Tree(name=node_name)
    ast.add_feature('lineno',lineno)
    if children is None:
        return ast
    for i in children:
        if i.__class__.__name__ == 'TreeNode':
            ast.add_child(child=i)
        else:
            ast.add_child(name=i)
    # if lineno != -1:
    #    line_numbers[id(ast)] = lineno
    return ast


# wrapper function that checks if node represents numerical value
# returns true if leaf is an integer
def is_integer(node):
    leafs = node.get_leaf_names()
    if len(leafs) > 1:
        return False
    return isinstance(node.get_leaf_names()[0], int)


def get_integer_node_value(node):
    return node.get_leaf_names()[0]
