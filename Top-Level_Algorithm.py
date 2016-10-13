# TODO: Create a list `playerList` to note the order in which the players take turns.
# TODO: “Roll die” (use RNG) to decide who plays first - add players to playerList in corresponding order.

# TODO: Randomly select Heroes.
# TODO: Choose initial allotment of cards for both players (default 4 cards).
# TODO: Create variable `currentState` and initialize with the Hero selection and the card allotment.

# TODO: Create int variable `turn` to track how many turns (not plys - pairs of plys) have been elapsed.
# TODO: Create boolean variable `terminate` to note whether a terminal state has been reached.
# TODO: Create variable ``
# TODO: while (True): (run turns)
# TODO:     Create variable `nextState` to hold the next proposed state and initialize to currentState.
# TODO:     for (`playerIndx` in playerList): (note that the player that goes first is first in the list)
# Distribute cards and mana crystals (updates currentState, not playerList).
# TODO:         if (this is the first turn):
# TODO:             Give this player 4 cards.
# TODO:             if (this player goes second):
# TODO:                 Give this player 2 mana crystals.
# TODO:             else:
# TODO:                 Give this player 1 mana crystal.
# TODO:         else:
# TODO:             Give this player 1 card and `turn` mana crystal(s).
# Find the best next state.
# TODO:         if (this player is the main AI):
# TODO:             for (each `proposedNextState` yielded by successorFunction(currentState, playerIndx)):
# TODO:                 if (utilityFunction(proposedNextState, playerIndx) > utilityFunction(nextState, playerIndx)):
# TODO:                     nextState = proposedNextState
# TODO:         else: (choose nextState randomly)
# TODO:             `nextState` = successorFunctionRandom(currentState, playerIndx)
# Go to that state.
# TODO:         currentState = bestState
# Check if this is a terminal state.
# TODO:     if (terminalTest(currentState) == True):
# TODO:         return (Games should be run multiple times to average performance results. Those are not recorded here.)


