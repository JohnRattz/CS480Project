from Deck import Deck
from Card import *

class Player:

    def __init__(self, hero, cards, isFirstPlayer):
        self.hero = hero
        self.hp = 30
        self.deck = Deck(hero, cards)
        self.isFirstPlayer = isFirstPlayer
        self.hand = []
        self.inPlay = []
        self.manaCrystals = 0
        self.availableMana = 0

    def drawCard(self):
        self.hand.append(self.deck.getNextCard())

    def getCoin(self):
        self.hand.append(Spell(0, "Coin", False, 0, "NEUTRAL"))

    def playCard(self, card):
        print("play card")

    def getHand(self):
        return self.hand

    def getDeck(self):
        return self.deck

    def addManaCrystal(self):
        self.manaCrystals += 1

    def rechargeMana(self):
        self.availableMana = self.manaCrystals

    def canPlayCard(self):
        for card in self.hand:
            if card.getCost() <= self.availableMana:
                return True
        return False

    def hasActiveMinions(self):
        for card in self.inPlay:
            if card.canAttack():
                return True
        return False

    def isDead(self):
        self.hp < 1

    def receiveDamage(self, dmg):
        self.hp -= dmg

    def hasAvailableMoves(self):
        return (self.canPlayCard() or self.hasActiveMinions)

    def __repr__(self):
        return "Hero: {} First: {} \nHand({}): {} \nInPlay({}): {} \nCrystals: {} Mana: {}".format(self.hero, self.isFirstPlayer, len(self.hand), self.hand,len(self.inPlay), self.inPlay, self.manaCrystals, self.availableMana)