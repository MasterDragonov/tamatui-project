"""Shared game data that every state can reach."""


class Game:
    """Holds everything that must survive switching states."""

    def __init__(self):
        self.running = True
        self.player = None  # set later by Character creation
