# TODO: Create static variable to record the explored state space.
# This static variable

# NOTE: To implement an n-ply lookahead, the successor function may call itself and utilityFunction,
#       alternating the point of view between the current player and the other player as it descends the tree.
def successorFunction(currentState, playerIndx, turn):
    '''
    Based on the current state and which player is making the current ply,
    returns states (one per invocation) corresponding to card choices and uses.

    :param currentState: A variable of type State representing the current state.
    :param playerIndx: An integer denoting the player that is making the current ply.
    :return successorState: A variable of type State representing a potential next state.
    '''
    successorState = currentState

    # TODO: Conduct a DFS of the state space for card choices,
    # TODO: choosing the left-most state on each iteration until no more cards may be chosen.
    # One thing to remember to do here is to add `min(turn, 10)` mana crystals to the current player every ply.

        # Given that choice...
        # TODO: Conduct a DFS of the state space for card usage given the set of chosen cards,
        # TODO: choosing the left-most state on each iteration until no more decisions may be made.

    yield successorState

def successorFunctionRandom(currentState, playerIndx, turn):
    '''
    Based on the current state and which player is making the current ply,
    returns states (one per invocation) corresponding to card choices and uses.

    :param currentState: A variable of type State representing the current state.
    :param playerIndx: An integer denoting the player that is making the current ply.
    :return successorState: A variable of type State representing a potential next state.
    '''
    successorState = currentState

    # TODO: Conduct a DFS of the state space for card choices,
    # TODO: choosing the next state randomly on each iteration until no more cards may be chosen.
    # One thing to remember to do here is to add `min(turn, 10)` mana crystals to the current player every ply.

        # Given that choice...
        # TODO: Conduct a DFS of the state space for card usage given the set of chosen cards,
        # TODO: choosing the next state randomly on each iteration until no more decisions may be made.

    return successorState
