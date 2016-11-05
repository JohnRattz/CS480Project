import multiprocessing as mp
import random
import sys

from Node import Node
from utilityFunction import utilityFunction

MAX_INT = 2**31 - 1
MIN_INT = -2**31


def getNextStates(state):
    """
    Gets all possible next states for State `state`.

    :param state:       State       The current state for which next states are desired.
    :return nextStates: list[State] The possible next states for `state`.
    """
    # TODO: Get all next states.
    # One thing to remember to do here is to give `min(turn, 10)` mana crystals to the current player every ply.
    # NOTE: Mana crystals do not carry over from previous turns.
    return nextStates


def successorFunction(currentState, playerIndx, turn):
    """
    Based on the current state and which player is making the current ply,
    returns the best next state (one per invocation) corresponding to card choices and uses.

    :param currentState:    State   A variable of type State representing the current state.
    :param playerIndx:      int     The player that is making the current ply.
    :param turn:            int     The current turn number. Used to determine mana crystal allotment.
    :return successorState: State   A variable of type State representing the best next state for player `playerIndx`.
    """
    def alphabeta(node, depth, alpha, beta, maxPlayer, maxDepth):
        """
        Performs alpha-beta pruning.

        I realize this deviates from the code on Lecture 12, Slide 15, but
        follow that code meticulously and you should find that it would return
        3 (beta) from the node 5 from the left and 2 from the bottom in the example,
        whereas it should return 15 as the example actually shows.

        :param node:            Node    The current node.
        :param depth:           int     The number of edges traversed from the root to reach this node.
        :param alpha:           int     The highest attainable score for the maximizing player so far.
        :param beta:            int     The lowest attainable score for the minimizing player so far.
        :param maxPlayer:       bool    Determines whether the maximizing or minimizing player is making this ply.
        :param maxDepth:        int     The maximum depth to descend the tree. The depth at which nodes are evaluated
                                        using `utilityFunction`.
        :return:                int     Ultimately, the alpha-beta value of the tree of states with `node` at the root.
        """
        if depth == maxDepth:
            score = utilityFunction(node.getState)
            return score

        currentState = node.getState()
        childNodes = [Node(nextState, None) for nextState in getNextStates(currentState)]
        if len(childNodes):
            score = utilityFunction(node.getState)
            return score

        if maxPlayer:
            # Maximum value of child nodes of this max node.
            childNodesMax = MIN_INT
            for childNode in childNodes:
                childNodeVal = alphabeta(childNode, depth + 1, alpha, beta, False)
                if childNodeVal > childNodesMax:
                    childNodesMax = childNodeVal
                alpha = max(alpha, childNodeVal)
                if beta <= alpha:
                    break  # Beta cutoff
            # If this node is a child of the root, return alpha-beta value for this branch and this node's state.
            if depth == 1:
                return min(alpha, childNodesMax), node.getState()
            else:
                return min(alpha, childNodesMax)
        else:
            # Minimum value of child nodes of this min node.
            childNodesMin = MAX_INT
            for childNode in childNodes:
                childNodeVal = alphabeta(childNode, depth+1, alpha, beta, True)
                if childNodeVal < childNodesMin:
                    childNodesMin = childNodeVal
                beta = min(beta, childNodeVal)
                if beta <= alpha:
                    break  # Alpha cutoff
            # If this node is a child of the root, return alpha-beta value for this branch and this node's state.
            if depth == 1:
                return max(beta, childNodesMin), node.getState()
            else:
                return max(beta, childNodesMin)

    successorState = None

    childNodes = [Node(nextState, None) for nextState in getNextStates(currentState)]
    initialNode = Node(currentState, childNodes)
    # Python integers have arbitrary precision, so choose the min and max values for 32-bit integers.
    alpha = MIN_INT
    beta = MAX_INT
    # `maxDepth` determines N in the N-ply lookahead.
    maxDepth = 1

    # This is more general than just using `1` for the `maxPlayer` parameter of `alphabeta()`.
    # We may want to test the AI when playing against "itself".
    nextPlayerIndx = 1 if playerIndx == 0 else nextPlayerIndx = 0

    # Create a multiprocessing pool with the number of threads equal to the number of logical processors.
    pool = mp.Pool(mp.cpu_count())

    # Get the alpha-beta value of all child nodes in parallel.
    alpha_beta_state_tuples = [pool.apply(alphabeta, [childNode, 1, alpha, beta, bool(nextPlayerIndx), maxDepth])
                               for childNode in childNodes]
    # Sort on alpha-beta value.
    alpha_beta_state_tuples.sort(key=lambda x: x[0])

    # Player 0 picks among states with the maximum alpha-beta value.
    # Player 1 picks among states with the minimum alpha-beta value (when testing player 1 with non-random AI).
    if playerIndx == 0:
        successorState = alpha_beta_state_tuples[alpha_beta_state_tuples.size() - 1][1]
    else:
        successorState = alpha_beta_state_tuples[0][1]

    return successorState


def successorFunctionRandom(currentState, playerIndx, turn):
    """
    Based on the current state,
    returns a random next state (one per invocation) corresponding to card choices and uses.

    :param currentState: A variable of type State representing the current state.
    :param playerIndx: An integer denoting the player that is making the current ply.
    :return successorState: A variable of type State representing a potential next state.
    """
    nextStates = getNextStates(currentState)
    successorState = random.choice(nextStates)
    return successorState

