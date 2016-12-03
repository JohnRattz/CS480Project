from Top_Level_Algorithm import *
import globals
import time

def test_game_playing_AI():
    # TODO: (Cisco)
    # Run this AI multiple times and average results at various lookahead depths.
    # To vary the lookahead depth, change `maxDepth` from `globals.py`.

    #global maxDepth

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

def test_deck_evaluating_AI():
    # TODO: (Jerrod)
    # Run this AI against an equivalent AI for some number of randomly generated decks,
    # running multiple times per deck and averaging results for that deck.
    # The AIs run with fixed and equal lookahead depth (some reasonable value like 3 or 4).
    pass

def test_deck_choosing_AI():
    # TODO: (Bart)
    # Given that this is Bart's idea, I defer to him.
    pass

if __name__ == "__main__":
    test_game_playing_AI()
    pass