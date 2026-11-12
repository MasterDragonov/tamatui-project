"""TamaTUI RPG: starts curses and runs the game states."""
import curses

from game_data import Game
from states.title import TitleState


def setup_colors():
    """Create the colour pairs and return the tile -> colour lookup."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_RED, -1)  # player
    curses.init_pair(5, curses.COLOR_WHITE, -1)
    return {
        0: curses.color_pair(1),
        1: curses.color_pair(2),
        2: curses.color_pair(3),
        3: curses.color_pair(5),
    }


def draw_stack(screen, stack):
    """Draw visible states bottom to top, then show them at once."""
    screen.erase()
    start = len(stack) - 1
    while start > 0 and stack[start].is_overlay:
        start -= 1
    for state in stack[start:]:
        state.draw(screen)
    screen.refresh()


def apply_request(stack, game, state):
    """The only place where states are switched."""
    if state.request is None:
        return
    kind, new_state = state.request
    state.request = None
    if kind == "push":
        stack.append(new_state)
    elif kind == "pop":
        stack.pop()
    elif kind == "replace":
        stack[-1] = new_state
    elif kind == "quit":
        game.running = False


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    game = Game()
    game.color_map = setup_colors()
    stack = [TitleState(game)]

    while game.running and stack:
        draw_stack(stdscr, stack)
        top = stack[-1]
        key = stdscr.getch()
        top.handle_key(key)
        top.update()
        apply_request(stack, game, top)


if __name__ == "__main__":
    curses.wrapper(main)
