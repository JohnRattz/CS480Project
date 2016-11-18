class Card:
    """
    Represents the highest level of abstraction at which Cards may be considered in the program.

    Attributes:
        cost        int     The number of mana crystals that must be spent to put this card in play.
        name        string  The name of the card.
        isLegendary bool    Whether this card is legendary or not.
    """
    def __init__(self, cost, name, isLegendary):
        self._cost = cost
        self._name = name
        self._isLegendary = isLegendary

    def getCost(self):
        return self._cost

    def getName(self):
        return self._name

    def isLegendary(self):
        return self._isLegendary


class Hero(Card):
    """
    Represents a Hero Card.

    Hero type is currently not represented.

    Attributes:
        health int  The number of health points this Hero has remaining.
    """
    def __init__(self, cost, name, isLegendary, health):
        super().__init__(cost, name, isLegendary)
        self._health = health

    def getHealth(self):
        return self._health

    def reduceHealth(self, health):
        self._health -= health


class Minion(Card):
    """
    Represents a Minion type Card.

    Attributes:
        health int  The number of health points this Minion has remaining.
        attack int  The amount of health (and/or defense) lost by a Card attacked by this Minion.
    """
    def __init__(self, cost, name, isLegendary, health, attack):
        super().__init__(cost, name, isLegendary)
        self._health = health
        self._attack = attack

    def getHealth(self):
        return self._health

    def reduceHealth(self, health):
        self._health -= health

    def getAttack(self):
        return self._attack

    def attack(self, card):
        """
        Attack another card and receive an attack from that card if it can also attack.
        This Card, the other Card, or both may be left with health <= 0.
        """
        if hasattr(card, 'reduceHealth'):
            # Attack `card`.
            card.reduceHealth(self._attack)
            # Receive attack from `card`.
            if hasattr(card, 'attack'):
                self.reduceHealth(card.getAttack())
        else:
            raise AttributeError("Cannot attack Card without `health` attribute and `reduceHealth` function.")


class Spell(Card):
    """
    Represents a Spell type card.

    Attributes:
        attack      We will only be considering spell cards that do
                    fixed amounts of damage to one Card.
    """
    def __init__(self, cost, name, isLegendary, attack):
        super().__init__(cost, name, isLegendary)
        self._attack = attack

    def attack(self, card):
        """
        Attack another card. This Card, the other Card, or both may be left with health <= 0.
        """
        if hasattr(card, 'reduceHealth'):
            # Attack `card`.
            card.reduceHealth(self._attack)
        else:
            raise AttributeError("Cannot attack Card without `health` attribute and `reduceHealth` function.")
