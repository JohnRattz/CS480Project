class State:
    """
    Represents a possible state of the game.

    Attributes:
        cardsInPlay  list[list[Card]]   The Cards in play for both players, with the outer list indexed by the players.
        cardsInHand  list[list[Card]]   The Cards in the players' hands, with the outer list indexed by the players.
                                        `cardsInHand[playerIndx][0]` is always the Hero card for player `playerIndx`.
        manaCrystals list[int]          The number of mana crystals for both players.
        decks        list[list[Card]]   The decks for both players.
    """
    def __init__(self, cardsInPlay, cardsInHand, manaCrystals, decks):
        self._cardsInPlay = cardsInPlay
        self._cardsInHand = cardsInHand
        self._manaCrystals = manaCrystals
        self._decks = decks

    def getCardsInPlay(self, playerIndx=None):
        if playerIndx is not None:
            return self._cardsInPlay[playerIndx]
        return self._cardsInPlay

    def getCardsInHand(self, playerIndx=None):
        if playerIndx is not None:
            return self._cardsInHand[playerIndx]
        return self._cardsInHand

    def getManaCrystals(self, playerIndx=None):
        if playerIndx is not None:
            return self._manaCrystals[playerIndx]
        return self._manaCrystals

    def getCardsInDeck(self, playerIndx=None):
        if playerIndx is not None:
            return self._decks[playerIndx]
        return self._decks
