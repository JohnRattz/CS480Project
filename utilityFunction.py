from Card import *
from globals import MAX_INT, MIN_INT

# TODO: Finish this. (Jerrod, Cisco)
def utilityFunction(state):
    '''
    Calculates a utility value for a state.
    Higher utility values indicate more preferred states
    for player 1 (more likely to be chosen when `playerIndx == 1`).
    That is, player 1 is MAX and player 0 is MIN.

    :param state:           State   The state to evaluate.
    :return utilityValue:   int     The utility value of `state`. Higher values indicate
                                    more favorable states for player 1.
    '''

    player0HeroHealth = state.getCardsInPlay(0)[0].getHealth()
    player1HeroHealth = state.getCardsInPlay(1)[0].getHealth()

    # Checks if it's a win state
    if (player0HeroHealth <= 0):
        # State favors player1
        return MAX_INT
    elif (player1HeroHealth <= 0):
        # State favors player0
        return MIN_INT

    # Calculates current/future player attacks
    # player0Attacks = calculateCardsGrade(state.getCardsInPlay(0))
    # player1Attacks = calculateCardsGrade(state.getCardsInPlay(1))

    # Updates hero health after current attacks are applied
    # player0HeroHealth = player0HeroHealth - player1Attacks[0]
    # player1HeroHealth = player1HeroHealth - player0Attacks[0]

    # Checks if it's a win state (again)
    if (player0HeroHealth <= 0):
        # State favors player1
        return MAX_INT
    elif (player1HeroHealth <= 0):
        # State favors player0
        return MIN_INT

    # Total mana crystal cost of this player's cards - excluding the Hero card.
    player0TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(0)[1:]])
    player1TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(1)[1:]])

    return (player1HeroHealth + player1TotalManaCrystalCost / 3) - (player0HeroHealth + player0TotalManaCrystalCost / 3)
    '''
    # Total mana crystal cost of this player's cards - excluding the Hero card.
    player0TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(0)[1:]])
    player1TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(1)[1:]])
    return (player1HeroHealth + player1TotalManaCrystalCost) - (player0HeroHealth + player0TotalManaCrystalCost)
    '''

# def calculateCardsGrade(cardsInPlay):
#     playerAttackNow = 0
#     playerAttackFuture = 0
#
#     # Sums the attacks of minion cards in play
#     for card in cardsInPlay:
#         if type(card) is Minion:
#             if (card.canAttack()):
#                 playerAttackNow += card.getAttack()
#             else:
#                 # Future attacks have half less weight
#                 playerAttackFuture += card.getAttack() * 0.25

    return [playerAttackNow, playerAttackFuture]