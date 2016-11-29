import multiprocessing as mp
import random
import itertools
import sys
from copy import deepcopy

from Card import *
from State import State
from utilityFunction import utilityFunction
from globals import heroesList, cardsList, maxDepth

MAX_INT = 2**31 - 1
MIN_INT = -2**31

def terminalTest(currentState):
    """
    Determines if `currentState` is a terminal state.

    :param currentState:    State   A variable of type State representing the current state.
    """
    # If either player's Hero card has no health, this is a terminal state
    firstPlayerHero = currentState.getCardsInPlay(0)[0]
    secondPlayerHero = currentState.getCardsInPlay(1)[0]
    if firstPlayerHero.getHealth() <= 0 or secondPlayerHero.getHealth() <= 0:
        return True
    return False


# TODO: Finish this. (John)
def getNextStates(currentState, playerIndx, turn):
    """
    Gets all possible next states for State `state`.

    :param currentState:    State       The current state for which next states are desired.
    :param playerIndx:      int         The player that is making the ply for this state.
    :param turn:            int         The current turn number. Used to determine mana crystal allotment.
    :return nextStates:     list[State] The possible next states for `state`.
    """
    global heroesList, cardsList
    # DEBUG
    # print("currentState: \n{}".format(currentState))
    # print("playerIndx: ", playerIndx)
    # print("turn: ", turn)
    # DEBUG

    # Avoid modifying `currentState` and create basis state for all next states.
    # It is used to prevent repeating mana crystal allotment and card allotment for each next state.
    nextStateBasis = deepcopy(currentState)
    currentPlayerHand = nextStateBasis.getCardsInHand(playerIndx)
    currentPlayerCardsInDeck = nextStateBasis.getCardsInDeck(playerIndx)

    if turn > 1:
        # Allot mana crystals.
        nextStateBasis.setManaCrystals(min(turn, 10), playerIndx)

        # Randomly chose a card for the player making this ply.
        if len(currentPlayerCardsInDeck) > 0:
            chosenCardIndx = random.choice(range(len(currentPlayerCardsInDeck)))
            # print("chosenCardIndx: ", chosenCardIndx)
            # Copy so that the following `del` does not delete this card.
            dealtCard = deepcopy(currentPlayerCardsInDeck[chosenCardIndx])
            # Remove selected Card from the deck.
            # chosenCardIndices.sort(reverse=True)
            # for cardIndx in chosenCardIndices:
            #     del cardsInDeck[cardIndx]
            del currentPlayerCardsInDeck[chosenCardIndx]
            # If a player has more than 10 cards in hand, any drawn cards are discarded.
            if len(currentPlayerHand) < 10:
                currentPlayerHand.append(dealtCard)

    cardCosts = [cardInHand.getCost() for cardInHand in currentPlayerHand]
    currentPlayerCardsInPlay = nextStateBasis.getCardsInPlay(playerIndx)
    currentPlayerCrystals = nextStateBasis.getManaCrystals(playerIndx)
    enemyPlayerIndx = 1 if playerIndx == 0 else 0
    enemyCardsInPlay = nextStateBasis.getCardsInPlay(enemyPlayerIndx)

    # Determine if this player has a weapon in play.
    currentPlayerHasWeapon = False
    for card in currentPlayerCardsInPlay:
        if isinstance(card, Weapon):
            currentPlayerHasWeapon = True
            break
    # Determine indices of this player's attack-capable cards in play.
    # (Select all cards but first since that is a Hero and the only attack-capable cards that can be
    #  in play at the beginning of a turn are Minions and Weapons)
    # TODO: Remove this line.
    # attackCapableCardIndices = list(range(1, len(currentPlayerCardsInPlay)))

    # DEBUG
    # print("nextStateBasis: \n{}".format(nextStateBasis))
    # DEBUG

    # For each possible set of card choices for this player (cards in hand - to be put in play)...
    # NOTE: For 10 cards in hand, these two loops (as written currently) run 1024 times.
    #       For 5 cards in hand, they run only 30 times.
    for numToChooseFromHand in range(0, min(len(currentPlayerHand), 7 - len(currentPlayerCardsInPlay)) + 1):
        for cardsToChooseIndices in itertools.combinations(range(len(currentPlayerHand)), numToChooseFromHand):
            cardsToChoose = [currentPlayerHand[cardIndx] for cardIndx in cardsToChooseIndices]
            # The maximum number of cards in play for one player is 7. This excludes weapon cards, and spell
            # cards are consumed on use. Thus, only chosen minion cards add to the number of cards in play.
            numCardsToPutInPlay = 0
            weaponChosenWhileWeaponInPlay = False
            # A list of indices of the chosen cards that are attack-capable this turn.
            newAttackCapableCardIndices = []
            # A list of indices of the chosen cards that *must* attack this turn (i.e. Spell cards).
            requiredAttackingCardIndices = []
            for cardIndx in range(len(cardsToChoose)):
                card = cardsToChoose[cardIndx]
                if isinstance(card, Minion):
                    numCardsToPutInPlay += 1
                if isinstance(card, Weapon):
                    if currentPlayerHasWeapon:
                        weaponChosenWhileWeaponInPlay = True
                        break
                    # Weapon cards allow the Hero to attack in the same ply in which the Weapon card is deployed.
                    newAttackCapableCardIndices.append(len(currentPlayerCardsInPlay) + cardIndx)
                if isinstance(card, Spell):
                    newAttackCapableCardIndices.append(len(currentPlayerCardsInPlay) + cardIndx)
                    requiredAttackingCardIndices.append(len(currentPlayerCardsInPlay) + cardIndx)

            numCurrentPlayerCardsInPlay = len(currentPlayerCardsInPlay) + numCardsToPutInPlay
            # print("numCurrentPlayerCardsInPlay:", numCurrentPlayerCardsInPlay)
            if numCurrentPlayerCardsInPlay > 7 or weaponChosenWhileWeaponInPlay:
                continue

            chosenCardCosts = [cardToChoose.getCost() for cardToChoose in cardsToChoose]
            totalCost = sum(chosenCardCosts)
            # print("chosenCardCosts:", chosenCardCosts)
            # If there are enough manacrystals remaining to choose another card...
            # (In our limited versions of Hearthstone, there is never a reason to have remaining cards to choose -
            #  only partly because mana crystals do not carry over from turn to turn.)
            remainingCrystals = currentPlayerCrystals - totalCost
            # print("remainingCrystals:", remainingCrystals)
            if remainingCrystals < 0:
                continue  # Choose another set of cards.
            # If this player can still have more cards in play...
            if numCurrentPlayerCardsInPlay < 7:
                canChooseMoreCards = False
                # The costs of cards not chosen.
                unchosenCardCosts = [cardCosts[cardIndx] for cardIndx in range(len(cardCosts))
                                     if cardIndx not in cardsToChooseIndices]
                for cardCost in unchosenCardCosts:
                    if remainingCrystals >= cardCost:
                        canChooseMoreCards = True
                        break
                if canChooseMoreCards:
                    continue

            # DEBUG
            # print("Can't choose any more cards!")
            # DEBUG

            # Remove the chosen cards from the current player's hand for the next state.
            nextStateCurrentPlayerHand = [currentPlayerHand[cardIndx] for cardIndx in range(len(currentPlayerHand))
                                          if cardIndx not in cardsToChooseIndices]
            # print("len(currentPlayerHand): ", len(currentPlayerHand))
            # print("len(nextStateCurrentPlayerHand): ", len(nextStateCurrentPlayerHand))
            # Add the chosen cards to the cards in play for this player.
            nextStateCurrentPlayerCardsInPlay = currentPlayerCardsInPlay + cardsToChoose
            # print("len(currentPlayerCardsInPlay): ", len(currentPlayerCardsInPlay))
            # print("len(nextStateCurrentPlayerCardsInPlay): ", len(nextStateCurrentPlayerCardsInPlay))
            # TODO: If "Charge" ability is included, this will need to be altered.
            # Determine indices of this player's attack-capable cards in play.
            # (Of initial cards, select all cards but first since that is a Hero and the only attack-capable cards
            #  that can be in play at the beginning of a turn are Minions and Weapons)
            attackCapableCardIndices = list(range(1, len(currentPlayerCardsInPlay))) + newAttackCapableCardIndices
            # print("attackCapableCardIndices: ", attackCapableCardIndices)
            # attackCapableCardIndices = [cardIndx for cardIndx in range(len(nextStateCurrentPlayerCardsInPlay) - len(cardsToChoose))
            #                             if hasattr(nextStateCurrentPlayerCardsInPlay[cardIndx], 'attack')]
            # Get subset of enemy cards that are attackable.
            # attackableCards = [card for card in enemyCardsInPlay if hasattr(card, 'reduceHealth')]
            attackableCardIndices = [cardIndx for cardIndx in range(len(enemyCardsInPlay))
                                     if hasattr(enemyCardsInPlay[cardIndx], 'reduceHealth')]
            # print("attackableCardIndices: ", attackableCardIndices)
            # For each possible set of attack-capable cards (order of attack matters)...
            for numToChooseFromAttackCapable in range(0, len(attackCapableCardIndices) + 1):
                for attackCapableCardsToChooseIndices in itertools.permutations(attackCapableCardIndices,
                                                                                numToChooseFromAttackCapable):
                    # Some cards must attack on deployment (Spell cards).
                    setRequiredAttackingCardIndices = set(requiredAttackingCardIndices)
                    # print("setRequiredAttackingCardIndices: ", setRequiredAttackingCardIndices)
                    setAttackCapableCardsToChooseIndices = set(attackCapableCardsToChooseIndices)
                    # print("setAttackCapableCardsToChooseIndices: ", setAttackCapableCardsToChooseIndices)
                    if not setRequiredAttackingCardIndices.issubset(setAttackCapableCardsToChooseIndices):
                        # print("Required card not included in attacking cards, skipping.")
                        continue

                    # For each combination of attackable cards (each card can only target one card)...
                    for attackableCardsToChooseIndices in itertools.combinations(attackableCardIndices,
                                                                                 numToChooseFromAttackCapable):
                        # Don't modify the original cards in `nextStateBasis`.
                        nextStateCurrentPlayerCardsInPlayAfterAttack = deepcopy(nextStateCurrentPlayerCardsInPlay)
                        nextStateEnemyCardsInPlayAfterAttack = deepcopy(enemyCardsInPlay)

                        attackingCards = [nextStateCurrentPlayerCardsInPlayAfterAttack[cardIndx] for cardIndx
                                          in attackCapableCardsToChooseIndices]
                        attackedCards = [nextStateEnemyCardsInPlayAfterAttack[cardIndx] for cardIndx
                                         in attackableCardsToChooseIndices]
                        # DEBUG
                        # print("nextStateCurrentPlayerCardsInPlayAfterAttack", nextStateCurrentPlayerCardsInPlayAfterAttack)
                        # print("nextStateEnemyCardsInPlayAfterAttack", nextStateEnemyCardsInPlayAfterAttack)
                        # print("attackCapableCardsToChooseIndices: ", attackCapableCardsToChooseIndices)
                        # print("attackableCardsToChooseIndices: ", attackableCardsToChooseIndices)
                        # print("attackingCards[:5]: ", attackingCards[:5])
                        # print("attackedCards[:5]: ", attackedCards[:5])
                        # DEBUG

                        # Attack the attackable cards with the attack-capable cards.
                        invalidAttack = False
                        for attackPairIndices in zip(attackCapableCardsToChooseIndices,
                                                     attackableCardsToChooseIndices):
                            # print("attackPairIndices: ", attackPairIndices)
                            attackingCardIndx = attackPairIndices[0]
                            attackedCardIndx = attackPairIndices[1]
                            attackingCard = nextStateCurrentPlayerCardsInPlayAfterAttack[attackingCardIndx]
                            attackedCard = nextStateEnemyCardsInPlayAfterAttack[attackedCardIndx]
                            # Check if the attacking card or attacked card already have no health or durability.
                            if hasattr(attackingCard, 'reduceHealth'):
                                if attackingCard.getHealth() <= 0:
                                    # A card with non-positive health or durability cannot attack (i.e. it was destroyed this turn).
                                    invalidAttack = True
                                    break
                            elif isinstance(attackingCard, Weapon):
                                if attackingCard.getDurability() <= 0:
                                    invalidAttack = True
                                    break
                            if attackedCard.getHealth() <= 0:
                                invalidAttack = True
                                break

                            attackingCard.attack(attackedCard)

                        if invalidAttack:
                            # Choose a different set of cards to attack (or a different set of attacking cards if all
                            # sets of cards to attack - given a set of attacking cards - have already been examined).
                            continue

                        # Remove all cards that have lost all of their health or durability (except Hero cards).
                        for attackPairIndices in zip(reversed(sorted(attackCapableCardsToChooseIndices)),
                                                     reversed(sorted(attackableCardsToChooseIndices))):
                            attackingCardIndx = attackPairIndices[0]
                            attackedCardIndx = attackPairIndices[1]
                            attackingCard = nextStateCurrentPlayerCardsInPlayAfterAttack[attackingCardIndx]
                            attackedCard = nextStateEnemyCardsInPlayAfterAttack[attackedCardIndx]

                            if hasattr(attackingCard, 'reduceHealth'):
                                if attackingCard.getHealth() <= 0 and not isinstance(attackingCard, Hero):
                                    del nextStateCurrentPlayerCardsInPlayAfterAttack[attackingCardIndx]
                            elif isinstance(attackingCard, Weapon):
                                if attackingCard.getDurability() <= 0:
                                    del nextStateCurrentPlayerCardsInPlayAfterAttack[attackingCardIndx]
                            else: # This is a Spell card. We only allow spell cards that are consumed on use.
                                del nextStateCurrentPlayerCardsInPlayAfterAttack[attackingCardIndx]
                            # Check the enemy player's cards in play.
                            if attackedCard.getHealth() <= 0 and not isinstance(attackedCard, Hero):
                                del nextStateEnemyCardsInPlayAfterAttack[attackedCardIndx]

                        # Assemble the next state.
                        # print("Assembling next state!")
                        # Get cards in play.
                        nextStateCardsInPlay = [0, 0]
                        nextStateCardsInPlay[playerIndx] = nextStateCurrentPlayerCardsInPlayAfterAttack
                        nextStateCardsInPlay[enemyPlayerIndx] = nextStateEnemyCardsInPlayAfterAttack

                        # Get cards in hand.
                        nextStateEnemyCardsInHand = nextStateBasis.getCardsInHand(enemyPlayerIndx)
                        nextStateCardsInHand = [0, 0]
                        nextStateCardsInHand[playerIndx] = nextStateCurrentPlayerHand
                        nextStateCardsInHand[enemyPlayerIndx] = nextStateEnemyCardsInHand

                        # Get mana crystals.
                        nextStateManaCrystals = [0, 0]
                        nextStateManaCrystals[playerIndx] = remainingCrystals
                        nextStateManaCrystals[enemyPlayerIndx] = nextStateBasis.getManaCrystals(enemyPlayerIndx)

                        # Get decks.
                        nextStateDecks = [0, 0]
                        nextStateDecks[playerIndx] = currentPlayerCardsInDeck
                        nextStateDecks[enemyPlayerIndx] = nextStateBasis.getCardsInDeck(enemyPlayerIndx)

                        nextState = State(nextStateCardsInPlay, nextStateCardsInHand,
                                          nextStateManaCrystals, nextStateDecks)
                        # print("nextState: ", nextState)
                        yield nextState

def alphabeta(currentState, playerIndx, turn, depth, alpha, beta, maxPlayer):#, maxDepth):
    """
    Performs alpha-beta pruning.

    I realize this deviates from the code on Lecture 12, Slide 15, but
    follow that code meticulously and you should find that it would return
    3 (beta) from the node 5 from the left and 2 from the bottom in the example,
    whereas it should return 15 as the example actually shows.

    :param currentState:    State   The current state.
    :param playerIndx:      int     The player that is making the current ply.
    :param turn:            int     The current turn number. Used to determine mana crystal allotment.
    :param depth:           int     The number of edges traversed from the root to reach this node.
    :param alpha:           int     The highest attainable score for the maximizing player so far.
    :param beta:            int     The lowest attainable score for the minimizing player so far.
    :param maxPlayer:       bool    Determines whether the maximizing or minimizing player is making this ply.
    :param maxDepth:        int     The maximum depth to descend the tree. The depth at which nodes are evaluated
                                    using `utilityFunction`.
    :return:                int     Ultimately, the alpha-beta value of the tree of states with `node` at the root.
    """
    global maxDepth

    if depth == maxDepth:
        # If this node is a child of the root (see context in `successorFunction`),
        # then return the state itself in addition to the alpha-beta value.
        if depth == 1:
            return utilityFunction(currentState), currentState
        return utilityFunction(currentState)

    # childNodes = [Node(nextState, None) for nextState in getNextStates(currentState, playerIndx, turn)]
    # if len(childNodes) == 0:
    #     score = utilityFunction(currentState)
    #     return score

    # The best value (whether MIN or MAX) for any child node.
    bestVal = None
    numChildren = 0
    if maxPlayer:
        # Maximum value of child nodes of this max node.
        bestVal = MIN_INT
        for childState in getNextStates(currentState, playerIndx, turn):
            numChildren += 1
            childStateVal = alphabeta(childState, playerIndx, turn, depth + 1, alpha, beta, False)#, maxDepth)
            if childStateVal > bestVal:
                bestVal = childStateVal
            alpha = max(alpha, childStateVal)
            if beta <= alpha:
                # print("Beta cutoff!")
                break  # Beta cutoff
        if numChildren == 0:
            if depth == 1:
                return utilityFunction(currentState), currentState
            return utilityFunction(currentState)
        if depth == 1:
            return min(alpha, bestVal), currentState
        else:
            return min(alpha, bestVal)
    else:
        # Minimum value of child nodes of this min node.
        bestVal = MAX_INT
        for childState in getNextStates(currentState, playerIndx, turn):
            numChildren += 1
            childStateVal = alphabeta(childState, playerIndx, turn, depth + 1, alpha, beta, True)#, maxDepth)
            if childStateVal < bestVal:
                bestVal = childStateVal
            beta = min(beta, childStateVal)
            if beta <= alpha:
                # print("Alpha cutoff!")
                break  # Alpha cutoff
        if numChildren == 0:
            if depth == 1:
                return utilityFunction(currentState), currentState
            return utilityFunction(currentState)
        if depth == 1:
            return max(beta, bestVal), currentState
        else:
            return max(beta, bestVal)

def successorFunction(currentState, playerIndx, firstPlayerIndx, turn):
    """
    Based on the current state and which player is making the current ply,
    returns the best next state (one per invocation) corresponding to card choices and uses.

    :param currentState:    State   A variable of type State representing the current state.
    :param playerIndx:      int     The player that is making the current ply.
    :param firstPlayerIndx: int     The index of the player making the first ply of every turn.
    :param turn:            int     The current turn number.
    :return successorState: State   A variable of type State representing the best next state for player `playerIndx`.
    """
    # childNodes = [Node(nextState, None) for nextState in getNextStates(currentState, playerIndx, turn)]
    # initialNode = Node(currentState, childNodes)
    childStates = [nextState for nextState in getNextStates(currentState, playerIndx, turn)]
    # print("len(childStates): ", len(childStates))
    # print("childStates: ", childStates)
    # Python integers have arbitrary precision, so choose the min and max values for 32-bit integers.
    alpha = MIN_INT
    beta = MAX_INT
    # `maxDepth` determines N in the N-ply lookahead.
    # maxDepth = 2

    # This is more general than just using `1` for the `maxPlayer` parameter of `alphabeta()`.
    # We may want to test the AI when playing against "itself".
    nextPlayerIndx = 1 if playerIndx == 0 else 0

    # Create a multiprocessing pool with the number of threads equal to the number of logical processors.
    pool = mp.Pool(mp.cpu_count())

    # Get the alpha-beta value of all child nodes in parallel (nodes for which the *next* player is making the ply).
    alpha_beta_state_tuples = [pool.apply(alphabeta, [childState, playerIndx, turn, 1,
                                                      alpha, beta, bool(nextPlayerIndx)])#, maxDepth])
                               for childState in childStates]
    pool.close()
    pool.join()

    # print("len(alpha_beta_state_tuples)", len(alpha_beta_state_tuples))
    # Sort on alpha-beta value.
    alpha_beta_state_tuples.sort(key=lambda x: x[0])
    print("len(alpha_beta_state_tuples):", len(alpha_beta_state_tuples))
    # print("alpha_beta_state_tuples[:3]:", alpha_beta_state_tuples[:3])
    # Player 0 picks among states with the minimum alpha-beta value.
    # Player 1 picks among states with the maximum alpha-beta value (when testing player 1 with non-random AI).
    successorState = None
    if playerIndx == 0:
        successorState = alpha_beta_state_tuples[0][1]
    else:
        successorState = alpha_beta_state_tuples[alpha_beta_state_tuples.size() - 1][1]

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
    nextStates = [nextState for nextState in getNextStates(currentState, playerIndx, turn)]
    # print("len(nextStates):", len(nextStates))
    successorState = random.choice(nextStates)
    return successorState


