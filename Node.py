from State import State

# TODO: Don't store a Node's children in itself.
# TODO: This class is very likely useless. Remove it whenever that is certain.
class Node:
    """
    Represents a node in the MiniMax search tree.

    Attributes:
        state       State       The state corresponding to this node.
        children    list[Node]  The child nodes of this node.
    """
    def __init__(self, state, children):
        self._state = state
        self._children = children

    def setState(self, state):
        self._state = state

    def getState(self):
        return self._state
