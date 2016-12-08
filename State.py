from copy import deepcopy
from utilityFunction import utilityFunction

# TODO: Include players.
class State:
    """
    Represents a possible state of the game.

    Attributes:
        players     list[Player] A list of two players - not necessarily in the order they play.
        heuristic   function     A heuristic function used to evaluate the utility value of states.
    """
    def __init__(self, players):
        """
        :param players: tuple[Player]   The game's players, in the order they play.
        """
        self._players = players
        self._heuristic = utilityFunction(self)

    def getPlayers(self):
        return self._players

    def getCardsInPlay(self, playerIndx=None):
        if playerIndx is not None:
            return self._players[playerIndx].getCardsInPlay()
        return self._players[0].getCardsInPlay(), self._players[1].getCardsInPlay()

# TODO: Everything below this line has not be rewritten yet (getCardsInPlay() has been rewritten).

#NOTE: Everything below this line has now been rewritten by Jerrod, but should certainly be held to
#a strict level of scrutiny, because this is Python and he's a noob in these parts.

    def getCardsInHand(self, playerIndx=None):
        if playerIndx is not None:
            return self._players[playerIndx].getHand()
        return self._players[0].getHand(), self._players[1].getHand()

    def getManaCrystals(self, playerIndx=None):
        if playerIndx is not None:
            return self._players[playerIndx].getAvailableMana()
        return self._players[0].getAvailableMana(), self._players[1].getAvailableMana()

    def setManaCrystals(self, num, playerIndx):
        self._players[playerIndx].setAvailableMana(num)
        self._heuristic = utilityFunction(self)

    def getCardsInDeck(self, playerIndx=None):
        if playerIndx is not None:
            return self._players[playerIndx].getDeck()
        return self._players[0].getDeck(), self._player[1].getDeck()

    def getHeuristic(self):
        return self._heuristic

    def __repr__(self):
        return  "cardsInPlay: \n{}".format("\n".join('{}'.format(item) for item in self.getCardsInPlay())) + "\n" + \
                "cardsInHand: \n{}".format("\n".join('{}'.format(item) for item in self.getCardsInHand())) + "\n" + \
                "manaCrystals: {}".format(self.getManaCrystals) + "\n" + \
                "decks: \n{}".format("\n".join('{}'.format(item) for item in self.getCardsInDeck())) + "\n"


# class State:
#     """
#     Represents a possible state of the game.
#
#     Attributes:
#         cardsInPlay  list[list[Card]]   The Cards in play for both players, with the outer list indexed by the players.
#         cardsInHand  list[list[Card]]   The Cards in the players' hands, with the outer list indexed by the players.
#                                         `cardsInHand[playerIndx][0]` is always the Hero card for player `playerIndx`.
#         manaCrystals list[int]          The number of mana crystals for both players.
#         decks        list[list[Card]]   The decks for both players.
#     """
#     def __init__(self, cardsInPlay, cardsInHand, manaCrystals, decks):
#         self._cardsInPlay = deepcopy(cardsInPlay)
#         self._cardsInHand = deepcopy(cardsInHand)
#         self._manaCrystals = deepcopy(manaCrystals)
#         self._decks = deepcopy(decks)
#         self._heuristic = utilityFunction(self)
#
#     def getCardsInPlay(self, playerIndx=None):
#         if playerIndx is not None:
#             return self._cardsInPlay[playerIndx]
#         return self._cardsInPlay
#
#     def getCardsInHand(self, playerIndx=None):
#         if playerIndx is not None:
#             return self._cardsInHand[playerIndx]
#         return self._cardsInHand
#
#     def getManaCrystals(self, playerIndx=None):
#         if playerIndx is not None:
#             return self._manaCrystals[playerIndx]
#         return self._manaCrystals
#
#     def setManaCrystals(self, num, playerIndx):
#         self._manaCrystals[playerIndx] = num
#         self._heuristic = utilityFunction(self)
#
#     def getCardsInDeck(self, playerIndx=None):
#         if playerIndx is not None:
#             return self._decks[playerIndx]
#         return self._decks
#
#     def getHeuristic(self):
#         return self._heuristic
#
#     def __repr__(self):
#         return  "cardsInPlay: \n{}".format("\n".join('{}'.format(item) for item in self._cardsInPlay)) + "\n" + \
#                 "cardsInHand: \n{}".format("\n".join('{}'.format(item) for item in self._cardsInHand)) + "\n" + \
#                 "manaCrystals: {}".format(self._manaCrystals) + "\n" + \
#                 "decks: \n{}".format("\n".join('{}'.format(item) for item in self._decks)) + "\n"
