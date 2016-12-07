import random
from Card import Card

class Deck:

    def __init__(self, hero, cards):
        self.hero = hero
        self.deckSize = 30
        self.deckCards = []
        self.createDeck(cards)
        self.shuffle()

    def createDeck(self, cards):
        filteredCards = self.removeOtherClassCards(cards)
        while len(self.deckCards) != self.deckSize:
            roll = random.randint(0, len(filteredCards) - 1)
            selectedCard = filteredCards[roll]
            score = self.evaluateCard(selectedCard)
            if score > 0:
                self.deckCards.append((selectedCard))

    def removeOtherClassCards(self, cards):
        filteredCards = []
        for card in cards:
            # TODO: Should "NEUTRAL" be in all caps?
            print("removeOtherClassCards: card.playerClass():". card.playerClass())
            if card.playerClass() == self.hero.getName() or card.playerClass() == "NEUTRAL":
                filteredCards.append(card)
        return filteredCards

    def evaluateCard(self, c):
        #TODO: complete evaluation
        if self.canAddCard(c):
            return 1
        return -1

    def canAddCard(self, card):
        # TODO: Doesn't this check for objects being the same rather than values?
        # You will have to define `__eq__()` to do this.
        if card.isLegendary() and card in self.deckCards:
            return False
        # Again, this checks for object address equality rather than value equality.
        if self.deckCards.count(card) > 1:
            return False
        return True

    def getNextCard(self):
        return self.deckCards.pop()

    def cardCount(self):
        return len(self.deckCards)

    def shuffle(self):
        random.shuffle(self.deckCards)

    def printSelf(self):
        for card in self.deckCards:
            print(card.getName())