"""The blueprint every game state follows."""


class State:
    """Base class: every state handles keys, updates and draws.

    A state never switches itself. It asks for a switch with one of
    the request methods, and the main loop carries it out.
    """

    is_overlay = False  # True: the state underneath stays visible

    def __init__(self, game):
        self.game = game
        self.request = None

    # --- the three jobs every state fills in ---
    def handle_key(self, key):
        """Decide what a key means in this state."""

    def update(self):
        """Change anything that needs changing this turn."""

    def draw(self, screen):
        """Draw this state onto the screen."""

    # --- switch requests, carried out by the main loop ---
    def push(self, state):
        """Put a new state on top of this one (e.g. open the menu)."""
        self.request = ("push", state)

    def pop(self):
        """Remove this state and go back to the one below."""
        self.request = ("pop", None)

    def replace(self, state):
        """Swap this state for a new one (e.g. title -> explore)."""
        self.request = ("replace", state)

    def quit(self):
        """End the game."""
        self.request = ("quit", None)
