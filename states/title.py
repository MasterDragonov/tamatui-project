"""Title screen: the first thing the player sees."""
import curses

from states.base import State

GAME_NAME = "QUEST OF THE TUI"
ENTER_KEYS = (curses.KEY_ENTER, 10, 13)


class TitleState(State):
    """Game name plus a New Game / Quit menu."""

    def __init__(self, game):
        super().__init__(game)
        self.options = ["New Game", "Quit"]
        self.selected = 0
        self.message = ""

    def handle_key(self, key):
        if key in (curses.KEY_UP, ord("w")):
            self.selected = (self.selected - 1) % len(self.options)
        elif key in (curses.KEY_DOWN, ord("s")):
            self.selected = (self.selected + 1) % len(self.options)
        elif key in ENTER_KEYS:
            choice = self.options[self.selected]
            if choice == "Quit":
                self.quit()
            elif choice == "New Game":
                # Next step: switch to Character creation / Explore here.
                self.message = "New Game coming soon!"

    def draw(self, screen):
        max_y, max_x = screen.getmaxyx()
        centre_y = max_y // 2

        draw_centred(screen, centre_y - 3, GAME_NAME, curses.A_BOLD)

        for i, option in enumerate(self.options):
            attr = curses.A_REVERSE if i == self.selected else 0
            draw_centred(screen, centre_y + i, f" {option} ", attr)

        draw_centred(screen, centre_y + 4, "Arrows/W/S to move, Enter to pick")
        draw_centred(screen, centre_y + 6, self.message)


def draw_centred(screen, y, text, attr=0):
    """Draw text centred on row y, skipping it if it doesn't fit."""
    max_y, max_x = screen.getmaxyx()
    x = (max_x - len(text)) // 2
    if 0 <= y < max_y - 1 and x >= 0:
        screen.addstr(y, x, text, attr)
