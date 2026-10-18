"""Core Memory Match rules, separated from the graphical interface."""

class GameState:
    """Store the game state and process player answers."""

    def __init__(self, first_cards=None):
        self.cards = list(first_cards) if first_cards is not None else ["star", "heart", "star"]
        if len(self.cards) != 3:
            raise ValueError("The game must start with exactly three cards.")
        self.score = 0
        self.level = 1
        self.progress = 0
        self.revealed_all = True
        self.game_active = True

    def submit_answer(self, said_match, new_card):
        """Check YES/NO, update score and progress, then shift in the next card."""
        if not self.game_active:
            return None
        is_match = self.cards[0] == self.cards[2]
        is_correct = (said_match == is_match)
        if is_correct:
            self.score += 50 * self.level
            self.progress += 1
            if self.progress >= 4:
                self.level += 1
                self.progress = 0
        else:
            if self.progress == 0 and self.level > 1:
                self.level -= 1
            self.progress = 0
        self.cards = [self.cards[1], self.cards[2], new_card]
        self.revealed_all = not is_correct
        return is_correct

    def end_session(self):
        """Finish the game and return the level-based bonus."""
        if not self.game_active:
            return 0
        bonus = 250 * self.level
        self.score += bonus
        self.game_active = False
        self.revealed_all = True
        return bonus
