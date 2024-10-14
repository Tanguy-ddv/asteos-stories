import pygaming
import pygame

from common.constants import STORE




class StoreFrame(pygaming.Frame):

    def __init__(self, master: pygaming.GamePhase | pygaming.Frame, window: pygame.Rect, background: pygaming.AnimatedSurface | pygame.Surface, focused_background: pygaming.AnimatedSurface | pygame.Surface | None = None, background_window: pygame.Rect | None = None, layer: int = 0, continue_animation: bool = False) -> None:
        super().__init__(master, window, background, focused_background, background_window, layer, continue_animation)




class StorePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(STORE, game)