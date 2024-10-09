"""Use this file to create a game."""
from pygaming import Game
from phases.menu import MenuGamePhase
from phases.connect import ConnectGamePhase

gm = Game(first_phase="connect", debug = True)
ConnectGamePhase(gm)
MenuGamePhase(gm)
gm.run()
