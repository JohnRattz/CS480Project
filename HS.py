import random
from Card import Card
from Player import Player
from Deck import Deck
from CardImport import loadCards, populatHeroesList
from State import State
from successorFunction import *
from utilityFunction import utilityFunction
import globals


def playGame(printStats = True):
    numInitialCardsPerPlayer = 3
    allCards = loadCards()
    heroes = []
    populatHeroesList(heroes)
    print(len(globals.heroesList))
    print(len(allCards))

    playerList = random.sample([0, 1], 2)

    playerOne = Player(getRandomElement(heroes), allCards, True)
    playerTwo = Player(getRandomElement(heroes), allCards, False)

    print(playerOne.hero)
    print(playerTwo.hero)

    for i in range(0, numInitialCardsPerPlayer):
        playerOne.drawCard()
        playerTwo.drawCard()
    playerTwo.getCoin()

    print(playerOne.getHand())
    print(playerTwo.getHand())

    turnCount = 0
    gameOver = False
    currentPlayer = None
    opponent = None
    ### start game
    while not gameOver:
        turnCount += 1

        if currentPlayer == playerOne:
            currentPlayer = playerTwo
            opponent = playerOne
        else:
            currentPlayer = playerOne
            opponent = playerTwo

        currentPlayer.addManaCrystal()
        currentPlayer.rechargeMana()
        currentPlayer.drawCard()

        print(currentPlayer)
        ##while currentPlayer.hasAvailableMoves():
        if currentPlayer.hasAvailableMoves():
            # successorFunction(currentPlayer, opponent, turn)
            print("get next move from successor function and execute")
            cardToPlay = currentPlayer.getHand()[0]
            currentPlayer.playCard(cardToPlay)
            if (opponent.isDead()):
                gameOver = True

        currentPlayer.refreshCardsInPlay()
        gameOver = turnCount == 10



    '''

    # Create variable of type State `currentState` and initialize with the Hero selection and the card allotment.
    currentState = State(cardsInPlay, cardsInHand, manaCrystals, decks)


    # Run the game.
    while not terminate:
        # Create variable `nextState` to hold the next proposed state.
        nextState = None
        for playerIndx in playerList:
            # Find the best next state.
            # If this player is the main AI...
            if playerIndx == 0:
                # Get next state based on MiniMax algorithm.
                nextState = successorFunction(currentState, playerIndx, firstPlayerIndx, turn)
            else: # choose nextState randomly for the other AI
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
    return playerIndx, turn, currentState
    '''

def getRandomElement(list):
    index = random.randint(0, len(list)-1)
    return list[index]

if __name__ == "__main__":
    # Run game playing AI by default, but these are supposed to be imported and tested in `testing.py`.
    # game_playing_AI()
    playGame()



