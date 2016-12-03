
class Agent(object):
    def __init__(self, hero, deck, state):
        self.hero = hero
        self.deck = deck
    
    def get_available_mana(self):
        return 0

    def get_turn_count(self):
        return 0
    
    def evaluate_board(self):
        return 0
    
    def can_win_this_turn(self):
        return False
    
    def can_loose_with_current_board(self):
        return False
    
    def get_this_turn_max_damage(self):
        return 0

    def get_minion_on_board_damage(self):
        return 0

    def get_damage_from_hand(self):
        return 0

    def create_decision_tree(self):
        return 0
    
    def get_current_hand(self):
        return 0