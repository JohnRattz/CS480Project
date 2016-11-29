# TODO: Finish this. (Jerrod, Cisco)
def utilityFunction(state):
    '''
    Calculates a utility value for a state.
    Higher utility values indicate more preferred states
    for player 1 (more likely to be chosen when `playerIndx == 1`).

    :param state:           State   The state to evaluate.
    :return utilityValue:   int     The utility value of state. Higher values indicate
                                    more favorable states for player 1.
    '''
    # TODO: Game Logic...
    # TODO: return utilityValue

    # Remove this when the utility function is completed - it only serves as a placeholder.
    # It only *vaguely* reflects the state of the game.
    player0HeroHealth = state.getCardsInPlay(0)[0].getHealth()
    player1HeroHealth = state.getCardsInPlay(1)[0].getHealth()
    # Total mana crystal cost of this player's cards - excluding the Hero card.
    player0TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(0)[1:]])
    player1TotalManaCrystalCost = sum([card.getCost() for card in state.getCardsInPlay(1)[1:]])
    return (player1HeroHealth + player1TotalManaCrystalCost) - (player0HeroHealth + player0TotalManaCrystalCost)