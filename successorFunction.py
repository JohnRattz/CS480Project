# TODO: Create static variable to record the explored state space.

# successorFunction and successorFunctionRandom may be able to be merged into one function.
def successorFunction(currentState, playerIndx):
    '''
    Based on the current state and which player is making the current ply,
    returns states (one per invocation) corresponding to card choices and uses.

    :param currentState: A variable of type State representing the current state.
    :param playerIndx: An integer denoting the player that is making the current ply.
    :return state: A variable of type State representing a potential next state.
    '''
    # TODO: Create variable of type State `state`.

    # TODO: Conduct a DFS of the state space for card choices,
    # TODO: choosing the left-most card on each iteration until no more cards may be chosen.

    # TODO: Conduct a DFS of the state space for card usage given the set of chosen cards
    # TODO: choosing the left-most card on each iteration until no more decisions may be made.

    # TODO: return state

def successorFunctionRandom(currentState, playerIndx):
    '''
    Based on the current state and which player is making the current ply,
    returns states (one per invocation) corresponding to card choices and uses.

    :param currentState: A variable of type State representing the current state.
    :param playerIndx: An integer denoting the player that is making the current ply.
    :return state: A variable of type State representing a potential next state.
    '''
    # TODO: Create variable of type State `state`.

    # TODO: Conduct a DFS of the state space for card choices,
    # TODO: choosing the next card randomly on each iteration until no more cards may be chosen.

    # TODO: Conduct a DFS of the state space for card usage given the set of chosen cards
    # TODO: choosing the next card randomly on each iteration until no more decisions may be made.

    # TODO: return state
