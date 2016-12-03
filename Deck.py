import random
import Card

class Deck:
    deckSize = 30

    def __init__(self, hero, cards):
        self.hero = hero
        self.deckCards = []
        self.createDeck(cards)
        self.shuffle()

    def createDeck(self, cards):
        deck = []
        filteredCards = self.removeOtherClassCards(cards)
        while len(deck) != self.deckSize:
            selectedCard = filteredCards[random.randint(0, len(filteredCards))]
            score = self.evaluateCard(deck, selectedCard)
            if score > 0:
                deck.append((selectedCard))
        return deck

    def removeOtherClassCards(self, cards):
        filteredCards = []
        for card in cards:
            if card.playerClass() == self.hero.getName() or card.playerClass() == "NEUTRAL":
                filteredCards.append(card)
        return filteredCards

    def evaluateCard(self, c):
        #TODO: complete evaluation
        if self.canAddCard(c):
            return 1
        return -1

    def canAddCard(self, card):
        if card.isLegendary() and card in self.deckCards:
            return False
        if self.deckCards.count(c) > 1:
            return False
        return True

    def getNextCard(self):
        return self.deckCards.pop()

    def cardCount(self):
        return len(self.deckCards)

    def shuffle(self):
        print "Shuffling deck"