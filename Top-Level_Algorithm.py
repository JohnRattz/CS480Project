# TODO: (Can we do this? Are the Hero cards in the dataset?) Randomly select Heroes (different abilities).
# TODO: “Roll die” (use RNG) to decide who plays first.
# TODO: Choose initial allotment of cards for both players (default 4 cards) and provide
#       1 extra mana crystal to player that goes second (only on first ply).
# TODO: Create some variables - namely:
# TODO:     Create a list `playerList` with proper player order.
# TODO:     Create int variable `turn` to track how many turns (not plys - pairs of plys) have been elapsed.
# TODO:     Create boolean variable `terminate` to note whether a terminal state has been reached.
# TODO:     Create variable `currentState` to hold the current state ("state" here means a card selection and play).
# TODO:     Create variable `bestState` to hold the best state.
# TODO: while (True): (run turns)
# TODO:     for (`player` in playerList): (note that the player that goes first is first in the list)
# Distribute cards and mana crystals.
# TODO:         if (this is the first turn):
# TODO:             Give this player 4 cards.
# TODO:             if (this player goes second):
# TODO:                 Give this player 2 mana crystals.
# TODO:             else:
# TODO:                 Give this player 1 mana crystal.
# TODO:         else:
# TODO:             Give this player 1 card and `turn` mana crystal(s).
# Find the best next state.
# TODO:         if (ths player is the main AI):
# TODO:             for (each `nextState` yielded by successorFunction(currentState)):
# TODO:                 if (utilityFunction(nextState) > utilityFunction(bestState)):
# TODO:                     bestState = nextState
# TODO:
# Go to that state.
# TODO: currentState = bestState

If (TerminalTest == True)
