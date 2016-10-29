import random
import Card
from State import State
from successorFunction import *
from utilityFunction import utilityFunction

def terminalTest(currentState):
    """
    Determines if `currentState` is a terminal state.
    """
    # If either player's Hero card has no health, this is a terminal state
    firstPlayerHero = currentState.getCardsInPlay(0)[0]
    secondPlayerHero = currentState.getCardsInPlay(1)[0]
    if firstPlayerHero.getHealth() == 0 or secondPlayerHero.getHealth() == 0:
        return True
    return False

def main():
    # Create a list `playerList` to note the order in which the players take turns (so either [0,1] or [1,0]).
    # The order is decided randomly.
    playerList = random.sample([0,1], 2)

    # TODO: Construct list of Heroes `heroesList` from the JSON data (joshuajharris)

    # TODO: Construct list of Cards `cardsList` from the JSON data (excluding Hero cards) (joshuajharris)

    # Randomly select Heroes and assign them to the players.
    # `cardsInHand[playerIndx][0]` is always the Hero card for player `playerIndx`.
    cardsInPlay = []
    selectedHeroes = random.sample(heroesList, 2)
    cardsInPlay.append([selectedHeroes[0]])
    cardsInPlay.append([selectedHeroes[1]])

    # Choose initial allotment of cards for both players (default 4 cards).
    initialCardAllotment = random.sample(cardsList, 8)
    chosenCardIndices = random.sample(range(8), 4)
    # Allot Cards for first player.
    cardsInHand = [[initialCardAllotment[chosenCardIndx] for chosenCardIndx in chosenCardIndices]]
    # Remove those selected Cards from `initialCardAllotment`.
    chosenCardIndices.sort(reverse=True)
    for cardIndx in chosenCardIndices:
        del initialCardAllotment[cardIndx]
    # Allot remaining Cards for second player.
    cardsInHand.append(initialCardAllotment)
    print("cardsInPlay: ", cardsInPlay)
    print("cardsInHand: ", cardsInHand)

    # Give both players mana crystals (1 for first player, 2 for second player).
    manaCrystals = [1, 2]

    # Create variable of type State `currentState` and initialize with the Hero selection and the card allotment.
    currentState = State(cardsInPlay, cardsInHand, manaCrystals)

    # `turn` tracks how many turns (not plys - pairs of plys) have been elapsed.
    turn = 0
    # `terminate` notes whether a terminal state has been reached.
    terminate = False

    # Run the game.
    while not terminate:
        # Create variable `nextState` to hold the next proposed state.
        nextState = None
        for playerIndx in playerList:
            # Find the best next state.
            # If this player is the main AI...
            if playerIndx == 0:
                # Get next state based on MiniMax algorithm.
                nextState = successorFunction(currentState, playerIndx, turn)
                # for proposedNextState in successorFunction(currentState, playerIndx, turn):
                    # If this state is better than the current state...
                    # if utilityFunction(proposedNextState) > utilityFunction(currentState):
                    #     nextState = proposedNextState
            else: # choose nextState randomly for the other AI
                nextState = successorFunctionRandom(currentState, playerIndx, turn)
            # Go to that state.
            currentState = nextState
            # Check if this is a terminal state.
            terminate = terminalTest(currentState)
        turn += 1

    # Return the last state for analysis purposes (in testing).
    return currentState

if __name__ is "__main__":
    main()
