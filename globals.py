# Max int, min int values
MAX_INT = 2**31 - 1
MIN_INT = -2**31

# List of Heroes `heroesList` from the JSON data - one instance of each Hero
heroesList = []
# Construct list of Cards `cardsList` from the JSON data - one instance of each card,
# only including minions and excluding Hero cards
cardsList = []

# The maximum lookahead depth in the minimax algorithm.
# maxDepth = 3

# def setMaxDepth(max):
#     global maxDepth
#     maxDepth = max