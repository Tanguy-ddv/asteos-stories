"""Use this file to create a game."""
from pygaming import Game
from menu import MenuGamePhase
from connect import Connect

gm = Game(first_phase="connect", debug = True)
Connect(gm)
MenuGamePhase(gm)
gm.run()
