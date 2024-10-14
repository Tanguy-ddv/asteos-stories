"""Use this file to create a game."""
from pygaming import Game
from phases.menu import MenuGamePhase
from phases.connect import ConnectGamePhase
from phases.highscores import HighScoresGamePhase

gm = Game(first_phase="connect", debug = True)
ConnectGamePhase(gm)
MenuGamePhase(gm)
HighScoresGamePhase(gm)
gm.run()
