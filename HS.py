import random
from Card import Card
from Player import Player
from Deck import Deck
from CardImport import loadCards, populateHeroesList
from State import State
from successorFunction import *
from utilityFunction import utilityFunction
import globals

# TODO: Allow the following options:
# 1) Two AIs compete - each with their own lookahead depths.
# 2) One AI and the AI that chooses among next states "randomly" (uses `successorFunctionRandom()`) compete.
# See `game_playing_AI()` in `Top_Level_Algorithm.py` for what this refers to.
def playGame(printStats = True, maxDepth1=1, maxDepth2=None):
    numInitialCardsPerPlayer = 3
    allCards = loadCards()
    heroes = []
    populateHeroesList(heroes)
    print(len(globals.heroesList))
    print(len(allCards))

    playerList = random.sample([0, 1], 2)
    print("Player order:", playerList)

    # `bool(playerList[0/1])` determines whether or not that player goes first.
    playerOne = Player(random.choice(heroes), allCards, bool(playerList[1]))
    playerTwo = Player(random.choice(heroes), allCards, bool(playerList[0]))

    print(playerOne._hero)
    print(playerTwo._hero)

    for i in range(0, numInitialCardsPerPlayer):
        playerOne.drawCard()
        playerTwo.drawCard()
    playerTwo.getCoin()

    print("playerOne Initial Hand:", playerOne.getHand())
    print("playerTwo Initial Hand:", playerTwo.getHand())

    # Assemble initial state here.
    players = [playerOne, playerTwo]
    currentState = State(players)
    print("Initial state:", currentState)

    turnCount = 0
    gameOver = False
    currentPlayer = None
    opponent = None

    # Play the game.
    while not gameOver:
        turnCount += 1
        # Create variable `nextState` to hold the next proposed state.
        nextState = None

        # Make both plys.
        for currentPlayer in State.getPlayers():
            # if currentPlayer == playerOne:
            #     currentPlayer = playerTwo
            #     opponent = playerOne
            # else:
            #     currentPlayer = playerOne
            #     opponent = playerTwo

            currentPlayer.addManaCrystal()
            currentPlayer.rechargeMana()
            currentPlayer.drawCard()
            print("currentPlayer:", currentPlayer)

            # TODO: What parameters needed for `successorFunction` calls?
            # If this player is the main AI...
            if currentPlayer is playerOne:
                nextState = successorFunction(currentState, playerIndx, firstPlayerIndx, turn, maxDepth1)
            else:  # Choose nextState either randomly or using MiniMax for the other AI.
                if maxDepth2 is not None:
                    nextState = successorFunction(currentState, maxDepth2)
                else:
                    nextState = successorFunctionRandom(currentState, playerIndx, firstPlayerIndx, turn)

            # TODO: Continue copying the format from `Top_Level_Algorithm.py`.

            ##while currentPlayer.hasAvailableMoves():
            if currentPlayer.hasAvailableMoves():
                # successorFunction(currentPlayer, opponent, turn)
                print("get next move from successor function and execute")
                cardToPlay = currentPlayer.getHand()[0]
                currentPlayer.playCard(cardToPlay)
                if (opponent.isDead()):
                    gameOver = True

            currentPlayer.refreshCardsInPlay()

if __name__ == "__main__":
    # Run game playing AI by default, but these are supposed to be imported and tested in `testing.py`.
    playGame()



