from HS import *
import globals
import time
import os

def test_game_playing_AI():
    # TODO: (John, Cisco)
    # Run this AI multiple times and average results at various lookahead depths.
    # To vary the lookahead depth, change `maxDepth` from `globals.py`.

    """
    seed = time.time()
    random.seed(0)
    globals.setMaxDepth(3)
    MAX_RUNS = 5

    # Stats
    print("Game Playing AI Test")
    print("====================")
    print("Seed:", seed)
    print("Max depth:", globals.maxDepth)

    for i in range(MAX_RUNS):
        print("")

        # Runs game
        time_start = time.time()
        result = game_playing_AI(False)
        time_end = time.time()

        # Displays stats
        print("\nWinner was player", result[0], "on turn", result[1], "\nState:\n{}".format(result[2]))
        print("Run #", i, "ran for", (time_end - time_start), "seconds")
    """

    # The lookahead depths for the AI player(s).
    maxDepthsToTest = [1, 2, 3]

    # 1) Test the AI against an AI that chooses among next states "randomly".
    results = []
    for maxDepth in maxDepthsToTest:
        numGamesWon = 0
        avgTurnsElapsed = 0
        numRuns = 10
        for i in range(1, numRuns + 1):
            print(r'Game Playing AI Test - AI vs "Random" AI')
            print("====================")
            print("Lookahead Depth:", maxDepth)
            print("Iteration:", i)
            winningPlayerIndx, turnsElapsed = playGame(False, maxDepth)
            # If the first player (the AI under test) won the game...
            if winningPlayerIndx == 0:
                numGamesWon += 1
            avgTurnsElapsed += turnsElapsed
        # Record the results of the preceeding games.
        percentWinningGames = numGamesWon / numRuns
        avgTurnsElapsed /= numRuns
        results.append([percentWinningGames, avgTurnsElapsed])

    # Create the test results directory if it does not exist.
    testdir = "testresults"
    if not os.path.exists(testdir):
        os.makedirs(testdir)

    # Create and write to the file.
    with open(os.path.join(testdir, 'AI_vs_random_AI_results.csv'), 'w') as outfile:
        outfile.write("Data Format: % games won, average # turns elapsed\n\n")
        for vals in results.values():
            for val in vals:
                outfile.write(str(val) + " ")
            outfile.write("\n")

    # 2) Test the AI against another AI, varying the lookahead depth for one but not the other.
    results = []
    for maxDepth in maxDepthsToTest:
        numGamesWon = 0
        avgTurnsElapsed = 0
        numRuns = 10
        for i in range(1, numRuns + 1):
            print(r'Game Playing AI Test - AI vs AI')
            print("====================")
            print("Lookahead Depth:", maxDepth)
            print("Iteration:", i)
            # The second AI always runs with a lookahead depth of 1.
            winningPlayerIndx, turnsElapsed = game_playing_AI(False, maxDepth, 1)
            if winningPlayerIndx == 0:
                numGamesWon += 1
            avgTurnsElapsed += turnsElapsed
        # Record the results of the preceding games.
        percentWinningGames = numGamesWon / numRuns
        avgTurnsElapsed /= numRuns
        results.append([percentWinningGames, avgTurnsElapsed])

    # Create and write to the file.
    with open(os.path.join(testdir, 'AI_vs_random_AI_results.csv'), 'w') as outfile:
        outfile.write("Data Format: % games won, average # turns elapsed\n\n")
        for vals in results.values():
            for val in vals:
                outfile.write(str(val) + " ")
            outfile.write("\n")

# def test_deck_choosing_AI():
#     # TODO: (Bart)
#     # Given that this is Bart's idea, I defer to him.
#     # Below are some suggestions.
#
#     # 1) Test generated decks by having two equally capable AIs (same lookahead depth) use them against each other.
#
#     # TODO: Generate 3 to 5 decks.
#     # (I cannot guarantee even 5 will finish in time to draft the report - Python is slow.)
#     # TODO: For each deck, run it against the other decks 10 times for N=2 for both AI players and average results.
#     # (N>2 takes an hour or longer to run each game.)
#
#     # For 3 decks, that would require 30 games to be played (deck1 vs. deck2, deck1 vs. deck3, deck2 vs. deck3).
#
#     # 2) Test professional decks by having two equally capable AIs (same lookahead depth) use them against each other.
#
#     # I would pick at most five professional decks and test as was done for the first test.
#
#     pass

if __name__ == "__main__":
    test_game_playing_AI()