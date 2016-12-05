import random
from Card import Card
from Player import Player
from Deck import Deck
from CardImport import loadCards, populatHeroesList
from State import State
from successorFunction import *
from utilityFunction import utilityFunction
import globals

# TODO: Allow the following options:
# 1) Two AIs compete - each with their own lookahead depths.
# 2) One AI and the AI that chooses among next states "randomly" (uses `successorFunctionRandom()`) compete.
# See `game_playing_AI()` in `Top_Level_Algorithm.py` for what this refers to.
def playGame(printStats = True):
    numInitialCardsPerPlayer = 3
    allCards = loadCards()
    heroes = []
    populatHeroesList(heroes)
    print(len(globals.heroesList))
    print(len(allCards))

    playerList = random.sample([0, 1], 2)

    playerOne = Player(random.choice(heroes), allCards, True)
    playerTwo = Player(random.choice(heroes), allCards, False)

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

# TODO: Don't call this an AI if it does not use AI principles.
def deck_choosing_AI():
    """
    Given that this is Bart's idea, I defer to him.

    :return:
    """
    # TODO: (Bart, John)
    pass

if __name__ == "__main__":
    # Run game playing AI by default, but these are supposed to be imported and tested in `testing.py`.
    playGame()



