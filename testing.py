from Top_Level_Algorithm import *
import globals
import time
import os

def test_game_playing_AI_vs_random_AI():
    """
    Fist set of tests for the game playing AI.

    Test the AI against an opponent that chooses among next states pseudo-randomly
    (see `successorFunction.getNextStates()` for criteria for selecting next states to examine).
    """

    # Create the test results directory if it does not exist.
    testdir = "testresults"
    if not os.path.exists(testdir):
        os.makedirs(testdir)

    # The lookahead depths for the AI player(s).
    maxDepthsToTest = [1, 2, 3]
    numRuns = 10

    print(r'Game Playing AI Test - AI vs "Random" AI')
    print("====================")
    # Create the file and write results to it.
    with open(os.path.join(testdir, 'AI_vs_random_AI_results.csv'), 'w') as outfile:
        outfile.write("Data Format: % games won (fractional), average # turns elapsed, run time (in seconds).\n\n")
        outfile.write("Each line corresponds to a test of an AI with lookahead depths in [1, 2, 3].\n")
        outfile.write("So, first line corresponds to lookahead depth 1, second line corresponds to lookahead depth 2, etc.\n\n")

        for maxDepth in maxDepthsToTest:
            print("Lookahead Depth:", maxDepth)

            numGamesWon = 0
            avgTurnsElapsed = 0
            avgElapsedTime = 0
            for i in range(1, numRuns + 1):
                print("Iteration:", i)

                t0 = time.time()
                winningPlayerIndx, turnsElapsed = game_playing_AI(False, maxDepth)
                avgElapsedTime += time.time() - t0

                # If the first player (the AI under test) won the game...
                if winningPlayerIndx == 0:
                    numGamesWon += 1
                avgTurnsElapsed += turnsElapsed
            # Record the results of the preceeding games.
            percentWinningGames = numGamesWon / numRuns
            avgTurnsElapsed /= numRuns
            avgElapsedTime /= numRuns
            print("Results: percentWinningGames: {}, avgTurnsElapsed: {}, avgElapsedTime: {}"
                  .format(percentWinningGames, avgTurnsElapsed, avgElapsedTime))
            outfile.write(str(percentWinningGames) + " " + str(avgTurnsElapsed) + " " + str(avgElapsedTime) + "\n")
            # Flush early to see results as they are written to the file.
            outfile.flush()
            print("")

def test_game_playing_AI_vs_other_AI():
    """
    Second set of tests for the game playing AI.

    Test the AI against another AI, varying the lookahead depth for one but not the other.
    """

    # Create the test results directory if it does not exist.
    testdir = "testresults"
    if not os.path.exists(testdir):
        os.makedirs(testdir)

    # The lookahead depths for the AI players.
    maxDepthsToTest = [1, 2, 3]
    numRuns = 10

    print(r'Game Playing AI Test - AI vs AI')
    print("====================")
    # Create the file and write results to it.
    with open(os.path.join(testdir, 'AI_vs_AI_results.csv'), 'w') as outfile:
        outfile.write("Data Format: % games won (fractional), average # turns elapsed, run time (in seconds).\n")
        outfile.write("Each line corresponds to a unique combination of lookahead depths in [1, 2, 3].\n")
        outfile.write("So, in tuples of (player 1 lookahead, player 2 lookahead), that would be (1,1), (1,2), (1,3), (2,2), (2,3), (3,3).\n\n")

        # For each unique combination of lookahead depths we are testing...
        # Avoid testing the same combinations of lookahead depths (e.g. [1,2] and [2,1]).
        for maxDepth1Indx in range(len(maxDepthsToTest)):
            for maxDepth2Indx in range(maxDepth1Indx, len(maxDepthsToTest)):
                maxDepth1 = maxDepthsToTest[maxDepth1Indx]
                maxDepth2 = maxDepthsToTest[maxDepth2Indx]
                print("Lookahead Depths:".format(maxDepth1, maxDepth2))
                print("Player 1:", maxDepth1, "Player 2: ", maxDepth2)

                numGamesWon = 0
                avgTurnsElapsed = 0
                avgElapsedTime = 0
                for i in range(1, numRuns + 1):
                    print("Iteration:", i)

                    t0 = time.time()
                    winningPlayerIndx, turnsElapsed = game_playing_AI(False, maxDepth1, 1)
                    avgElapsedTime += time.time() - t0

                    if winningPlayerIndx == 0:
                        numGamesWon += 1
                    avgTurnsElapsed += turnsElapsed
                # Record the results of the preceding games.
                percentWinningGames = numGamesWon / numRuns
                avgTurnsElapsed /= numRuns
                avgElapsedTime /= numRuns
                print("Results: percentWinningGames: {}, avgTurnsElapsed: {}, avgElapsedTime: {}"
                      .format(percentWinningGames, avgTurnsElapsed, avgElapsedTime))
                outfile.write(str(percentWinningGames) + " " + str(avgTurnsElapsed) + " " + str(avgElapsedTime) + "\n")
                # Flush early to see results as they are written to the file.
                outfile.flush()
                print("")

if __name__ == "__main__":
    # test_game_playing_AI_vs_random_AI()
    test_game_playing_AI_vs_other_AI()