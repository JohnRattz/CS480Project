import multiprocessing as mp
import random
import itertools
import sys
from Node import Node
from utilityFunction import utilityFunction
from globals import heroesList, cardsList

MAX_INT = 2**31 - 1
MIN_INT = -2**31


# TODO: Finish this (jrattz)
# TODO: Make this a generator for DFS.
def getNextStates(state, playerIndx, turn):
    """
    Gets all possible next states for State `state`.

    :param state:           State   The current state for which next states are desired.
    :param playerIndx:      int     The player that is making the ply for this state.
    :param turn:            int     The current turn number. Used to determine mana crystal allotment.
    :return nextStates: list[State] The possible next states for `state`.
    """
    global heroesList, cardsList

    # Randomly chose a card for the player making this ply.
    cardsInDeck = state.getCardsInDeck(playerIndx)
    chosenCardIndx = random.choice(range(len(cardsInDeck)))
    dealtCard = cardsInDeck[chosenCardIndx]
    # Remove selected Card from the deck.
    # chosenCardIndices.sort(reverse=True)
    # for cardIndx in chosenCardIndices:
    #     del cardsInDeck[cardIndx]
    del cardsInDeck[chosenCardIndx]

    currentPlayerHand = state.getCardsInHand(playerIndx) + [dealtCard]
    cardCosts = [cardInHand.getCost() for cardInHand in currentPlayerHand]
    currentPlayerCardsInPlay = state.getCardsInPlay(playerIndx)
    currentPlayerCrystals = state.getManaCrystals(playerIndx)

    enemyPlayerIndx = 1 if playerIndx == 0 else 0
    enemyCardsInPlay = state.getCardsInPlay(enemyPlayerIndx)

    # TODO: For each possible set of card choices for this player (cards in hand - to be put in play)...
    # TODO: Include possibility for choosing no cards?
    # NOTE: For 10 cards in hand, these two loops (as written currently) run 1023 times.
    #       For 5 cards in hand, they run only 30 times.
    for numToChooseFromHand in range(1, len(currentPlayerHand) + 1):
        for cardsToChooseIndices in itertools.combinations(range(len(currentPlayerHand)), numToChooseFromHand):
            cardsToChoose = [currentPlayerHand[cardIndx] for cardIndx in cardsToChooseIndices]
            chosenCardCosts = [cardToChoose.getCost() for cardToChoose in cardsToChoose]
            print(chosenCardCosts)
            totalCost = sum(chosenCardCosts)
            # If there are enough manacrystals remaining to choose another card...
            # (In our limited versions of Hearthstone, there is never a reason to have remaining cards to choose -
            #  only partly because mana crystals do not carry over from turn to turn.)
            remainingCrystals = currentPlayerCrystals - totalCost

            canChooseMoreCards = False
            for cardCost in cardCosts:
                if remainingCrystals >= cardCost:
                    canChooseMoreCards = True
                    break
            if canChooseMoreCards:
                continue  # Choose another set of cards.

            # Add the chosen cards to the cards in play for this player.
            cardsInPlay = currentPlayerCardsInPlay + cardsToChoose
            # Get subset of the current player's cards that can attack.
            attackCapableCards = [card for card in cardsInPlay if hasattr(card, 'attack')]
            # Get subset of enemy cards that are attackable.
            attackableCards = [card for card in enemyCardsInPlay if hasattr(card, 'reduceHealth')]
            # TODO: For each possible set of attack-capable cards...
            for numToChooseFromAttackCapable in range(1, len(attackCapableCards) + 1):
                for attackCapableCardsToChoose in itertools.combinations(attackCapableCards,
                                                                         numToChooseFromAttackCapable):
                    # TODO: For each possible permutation of that set (order of attack matters)...
                        # TODO: For each possible combination of attackable cards (of this set's size)...
                            # TODO: Attack the attackable cards with the attack-capable cards.
                            # TODO: Give `min(turn, 10)` mana crystals to the other player.
                            # TODO: Add this state to `nextStates`.
                    continue

    # TODO: One thing to remember to do here is to give `min(turn, 10)` mana crystals to the current player every ply.
    # NOTE: Mana crystals do not carry over from previous turns.
    return nextStates

def successorFunction(currentState, playerIndx, firstPlayerIndx, turn):
    """
    Based on the current state and which player is making the current ply,
    returns the best next state (one per invocation) corresponding to card choices and uses.

    :param currentState:    State   A variable of type State representing the current state.
    :param playerIndx:      int     The player that is making the current ply.
    :param firstPlayerIndx: int     The index of the player making the first ply of every turn.
    :param turn:            int     The current turn number. Used to determine mana crystal allotment.
    :return successorState: State   A variable of type State representing the best next state for player `playerIndx`.
    """
    def alphabeta(currentState, depth, alpha, beta, maxPlayer, maxDepth):
        """
        Performs alpha-beta pruning.

        I realize this deviates from the code on Lecture 12, Slide 15, but
        follow that code meticulously and you should find that it would return
        3 (beta) from the node 5 from the left and 2 from the bottom in the example,
        whereas it should return 15 as the example actually shows.

        :param currentState:    State   The current state.
        :param depth:           int     The number of edges traversed from the root to reach this node.
        :param alpha:           int     The highest attainable score for the maximizing player so far.
        :param beta:            int     The lowest attainable score for the minimizing player so far.
        :param maxPlayer:       bool    Determines whether the maximizing or minimizing player is making this ply.
        :param maxDepth:        int     The maximum depth to descend the tree. The depth at which nodes are evaluated
                                        using `utilityFunction`.
        :return:                int     Ultimately, the alpha-beta value of the tree of states with `node` at the root.
        """
        if depth == maxDepth:
            score = utilityFunction(currentState)
            return score

        # childNodes = [Node(nextState, None) for nextState in getNextStates(currentState, playerIndx, turn)]
        # if len(childNodes) == 0:
        #     score = utilityFunction(currentState)
        #     return score

        for childState in getNextStates(currentState, playerIndx, turn):
            if maxPlayer:
                # Maximum value of child nodes of this max node.
                childNodesMax = MIN_INT
                for childNode in childNodes:
                    childNodeVal = alphabeta(childNode, depth + 1, alpha, beta, False, maxDepth)
                    if childNodeVal > childNodesMax:
                        childNodesMax = childNodeVal
                    alpha = max(alpha, childNodeVal)
                    if beta <= alpha:
                        break  # Beta cutoff
                # If this node is a child of the root, return alpha-beta value for this branch and this node's state.
                if depth == 1:
                    return min(alpha, childNodesMax), currentState
                else:
                    return min(alpha, childNodesMax)
            else:
                # Minimum value of child nodes of this min node.
                childNodesMin = MAX_INT
                for childNode in childNodes:
                    childNodeVal = alphabeta(childNode, depth+1, alpha, beta, True, maxDepth)
                    if childNodeVal < childNodesMin:
                        childNodesMin = childNodeVal
                    beta = min(beta, childNodeVal)
                    if beta <= alpha:
                        break  # Alpha cutoff
                # If this node is a child of the root, return alpha-beta value for this branch and this node's state.
                if depth == 1:
                    return max(beta, childNodesMin), currentState
                else:
                    return max(beta, childNodesMin)

    # childNodes = [Node(nextState, None) for nextState in getNextStates(currentState, playerIndx, turn)]
    # initialNode = Node(currentState, childNodes)
    childStates = [nextState for nextState in getNextStates(currentState, playerIndx, turn)]
    # Python integers have arbitrary precision, so choose the min and max values for 32-bit integers.
    alpha = MIN_INT
    beta = MAX_INT
    # `maxDepth` determines N in the N-ply lookahead.
    maxDepth = 1

    # This is more general than just using `1` for the `maxPlayer` parameter of `alphabeta()`.
    # We may want to test the AI when playing against "itself".
    nextPlayerIndx = 1 if playerIndx == 0 else 0

    # Create a multiprocessing pool with the number of threads equal to the number of logical processors.
    pool = mp.Pool(mp.cpu_count())

    # Get the alpha-beta value of all child nodes in parallel (nodes for which the *next* player is making the ply).
    alpha_beta_state_tuples = [pool.apply(alphabeta, [childState, 1, alpha, beta, bool(nextPlayerIndx), maxDepth])
                               for childState in childStates]
    # Sort on alpha-beta value.
    alpha_beta_state_tuples.sort(key=lambda x: x[0])

    # Player 0 picks among states with the maximum alpha-beta value.
    # Player 1 picks among states with the minimum alpha-beta value (when testing player 1 with non-random AI).
    successorState = None
    if playerIndx == 0:
        successorState = alpha_beta_state_tuples[alpha_beta_state_tuples.size() - 1][1]
    else:
        successorState = alpha_beta_state_tuples[0][1]

    return successorState

# TODO: May not need `firstPlayerIndx`.
def successorFunctionRandom(currentState, playerIndx, firstPlayerIndx, turn):
    """
    Based on the current state,
    returns a random next state (one per invocation) corresponding to card choices and uses.

    :param currentState:    State   A variable of type State representing the current state.
    :param playerIndx:      int     The player that is making the current ply.
    :param firstPlayerIndx: int     The index of the player making the first ply of every turn.
    :param turn:            int     The current turn number. Used to determine mana crystal allotment.
    :return successorState: State   A variable of type State representing the best next state for player `playerIndx`.
    """
    nextStates = getNextStates(currentState, playerIndx, turn)
    successorState = random.choice(nextStates)
    return successorState

