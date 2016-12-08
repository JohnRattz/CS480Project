from Player import Player
from Card import *


class Agent(object):
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
    
    def evaluateBoard(self):
        return 0
    
    def canWinThisTurn(self):
        if getMyMaxDamageThisTurn() >= opponent.getHP():
            return True
        return False
    
    def canLooseWithCurrentBoard(self):
        if getMinionOnBoardDamage(opponent) >= player.getHP():
            return True
        return False
    
    def getMyMaxDamageThisTurn(self):
        dmg = self.get_minion_on_board_damage(self.player)
        dmg += getDamageFromHand()
        return dmg

    def getMinionOnBoardDamage(self, player):
        dmg = 0
        for minion in player.inPlay():
            if minion.canAttack:
                dmg += minion.getAttack()
        return dmg

    def getDamageFromHand(self):
        return 0

    def createDecisionTree(self):
        return 0