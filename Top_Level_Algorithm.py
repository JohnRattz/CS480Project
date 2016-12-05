import random
import Card
from Deck import Deck
from CardImport import loadCards
from State import State
from successorFunction import *
from utilityFunction import utilityFunction
import globals

# TODO: HS.py supercedes this file. When this file is no longer valuable as a reference, delete it.

def game_playing_AI(printStats=True, maxDepth1=2, maxDepth2=None):
    """
    This AI plays Hearthstone with a subset of all possible cards.
    It is evaluated against a pseudo-random AI.

    :param printStats: bool Determines whether or not statistics are printed at the end of the game.
    :param maxDepth1:  int  The lookahead depth for the first AI.
    :param maxDepth2:  bool The lookahead depth for the second AI.

    :return (winningPlayer, endTurn): int, int  A tuple containing the winning player and the end turn number.
    """
    # Loads cards from json file
    loadCards()
    #print(len(globals.heroesList))
    #print(len(globals.cardsList))

    # Create a list `playerList` to note the order in which the players take turns (so either [0,1] or [1,0]).
    # The order is decided randomly.
    playerList = random.sample([0,1], 2)
    firstPlayerIndx = playerList[0]
    # Randomly select Heroes and assign them to the players.
    # `cardsInPlay[playerIndx][0]` is always the Hero card for player `playerIndx`.
    cardsInPlay = []
    selectedHeroes = random.sample(globals.heroesList, 2)
    cardsInPlay.append([selectedHeroes[0]])
    cardsInPlay.append([selectedHeroes[1]])

    # Generate decks for both players.
    deckSize = 30
    # First player's deck
    deck0 = Deck(selectedHeroes[0], cardsList)
    # Second player's deck
    deck1 = Deck(selectedHeroes[1], cardsList)

    # Choose initial allotment of cards for both players (default 4 cards per player).
    cardsInHand = []
    numInitialCardsPerPlayer = 3

    ####### code to replace the portion until line "decks = [deck0, deck1]"
    # cardsInHandP1 = []
    # cardsInHandP2 = [Card("Coin")]
    # for i in range(numInitialCardsPerPlayer):
    #   cardsInHandP1.append(deck0.getNextCard())
    #   cardsInHandP2.append(deck1.getNextCard())
    #######


    chosenCardIndices0 = random.sample(range(deckSize), numInitialCardsPerPlayer)
    chosenCardIndices1 = random.sample(range(deckSize), numInitialCardsPerPlayer)
    cardsInHand.append([deck0[chosenCardIndx] for chosenCardIndx in chosenCardIndices0])
    cardsInHand.append([deck1[chosenCardIndx] for chosenCardIndx in chosenCardIndices1])
    # Remove those selected Cards from the respective decks.
    chosenCardIndices0.sort(reverse=True)
    for cardIndx in chosenCardIndices0:
        del deck0[cardIndx]
    chosenCardIndices1.sort(reverse=True)
    for cardIndx in chosenCardIndices1:
        del deck1[cardIndx]

    decks = [deck0, deck1]
    print("cardsInPlay: ", cardsInPlay)
    print("cardsInHand: ", cardsInHand)
    print("len(deck0): ", len(deck0))
    print("len(deck1): ", len(deck1))

    # Give both players mana crystals (1 for first player, 2 for second player).
    manaCrystals = [0, 0]
    manaCrystals[playerList[0]] = 1
    manaCrystals[playerList[1]] = 2

    # Create variable of type State `currentState` and initialize with the Hero selection and the card allotment.
    currentState = State(cardsInPlay, cardsInHand, manaCrystals, decks)

    # `turn` tracks the current turn number.
    # (a ply is the set of choices for one player in a turn and turns are pairs of plys)
    turn = 1
    # `playerIndx` corresponds to the player making the current ply.
    playerIndx = playerList[0]
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
                nextState = successorFunction(currentState, playerIndx, firstPlayerIndx, turn, maxDepth1)
            else: # Choose nextState either randomly or using MiniMax for the other AI.
                if maxDepth2 is not None:
                    nextState = successorFunction(currentState, playerIndx, firstPlayerIndx, turn, maxDepth2)
                else:
                    nextState = successorFunctionRandom(currentState, playerIndx, firstPlayerIndx, turn)
            # Go to that state.
            currentState = nextState
            # Check if this is a terminal state.
            terminate = terminalTest(currentState)
            if terminate:
                break
        turn += 1

    # Prints winning state information
    if printStats:
        print("\nWinner was player", playerIndx, "on turn", turn, "with state:\n{}".format(currentState))

    # Return information for analysis purposes (in testing).
    # (Winning player index, ending turn, ending state)
    return playerIndx, turn#, currentState

if __name__ == "__main__":
    # Run game playing AI by default, but these are supposed to be imported and tested in `testing.py`.
    game_playing_AI()
