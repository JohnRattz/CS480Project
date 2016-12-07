from Deck import Deck
from Card import *

class Player:
    """
    Represents one of two players playing the game.

    Attributes:
        hero
    """

    def __init__(self, hero, cards, isFirstPlayer):
        self._hero = hero
        self._hp = 30
        self._deck = Deck(hero, cards)
        self._isFirstPlayer = isFirstPlayer
        self._hand = []
        self._inPlay = []
        self._manaCrystals = 0
        self._availableMana = 0

    def drawCard(self):
        self._hand.append(self._deck.getNextCard())

    # TODO: Include in second iteration - Spell cards not in first iteration.
    # def getCoin(self):
    #     self._hand.append(Spell(0, "Coin", False, 0, "NEUTRAL", ""))

    def getHero(self):
        return self._hero

    def getHP(self):
        return self._hp

    def getDeck(self):
        return self._deck

    def isFirstPlayer(self):
        return self._isFirstPlayer

    def getHand(self):
        return self._hand

    def getCardsInPlay(self):
        return self._inPlay

    def getManaCrystals(self):
        return self._manaCrystals

    def getAvailableMana(self):
        return self._availableMana

    def setAvailableMana(self, num):
        self._availableMana = num

    # TODO: Finish this (is it really needed?).
    def playCard(self, card):
        print("play card")

    def addManaCrystal(self):
        # The maximum number of mana crystals a player can have
        # and can be allotted at the beginning of a turn is 10.
        if self._manaCrystals < 10:
            self._manaCrystals += 1

    def rechargeMana(self):
        self._availableMana = self._manaCrystals

    def canPlayCard(self):
        for card in self._hand:
            if card.getCost() <= self._availableMana:
                if card.__class__.__name__ == "Minion" and not self.hasAvailableSlots():
                    return False
                return True
        return False

    def hasAvailableSlots(self):
        takenSlots = 0
        for c in self._inPlay:
            if c.__class__.__name__ == "Minion":
                takenSlots += 1
        return takenSlots < 7

    def hasActiveMinions(self):
        for card in self._inPlay:
            if card.canAttack():
                return True
        return False

    def isDead(self):
        self._hp < 1

    def receiveDamage(self, dmg):
        self._hp -= dmg

    def hasAvailableMoves(self):
        return (self.canPlayCard() or self.hasActiveMinions)

    def refreshCardsInPlay(self):
        for c in self._inPlay:
            if c.__class__.__name__ == "Minion":
                c.refreshCard()

    def playCard(self, card):
        if (card.getCost() <= self._availableMana):
            self._hand.remove(card)
            self._inPlay.append(card)
            self._availableMana -= card.getCost()
            print("Played: {}".format(card.getName()))
        else:
            print("Cannot play this card: {}".format(card.getName()))

    def __repr__(self):
        return "Hero: {} First: {} \nHand({}): {} \nInPlay({}): {} \nCrystals: {} Mana: {}".format\
            (self._hero, self._isFirstPlayer, len(self._hand), self._hand,
             len(self._inPlay), self._inPlay, self._manaCrystals, self._availableMana)
