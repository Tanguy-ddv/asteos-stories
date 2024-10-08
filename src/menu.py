import math

import pygaming
import pygame
from .common.constants import MENU, CREATE_GAME, LOBBY, HIGHSCORES, STORE


Y_POINTER = 300
POINTER_AMPLITUDE = 100
Y_LABEL = 150
X_POINTER = [170, 395, 620, 791, 890, 1015]
NEXT_PHASES = [CREATE_GAME, CREATE_GAME, LOBBY, HIGHSCORES, STORE, pygaming.NO_NEXT]


class Selector(pygaming.Actor):

    def __init__(self, master: pygaming.Frame) -> None:
        super().__init__(master, pygaming.ImageFile("menu_selector.png").get(rotation=180), X_POINTER[0], Y_POINTER, pygaming.CENTER, 1)
        self.time = 0
        self.pulsation = 2*math.pi*0.2
    
    def update(self, loop_duration: int):
        self.time += loop_duration
        self.translate(0, self.get_speed()/loop_duration)

    def get_speed(self):
        return math.cos(self.time*self.pulsation/1000)*self.pulsation*POINTER_AMPLITUDE

    def get_surface(self) -> pygame.Surface:
        return self.main_surface.get()

class MenuGamePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(MENU, game)
        menu_bg = pygaming.ImageFile("menu_background.png").get()
        font = pygaming.FontFile("Super Unicorn.ttf").get(30, (0, 0, 0, 0), self.settings)
        self.pointer_position = 0
        self.next_phase = pygaming.STAY
        self.background_frame = pygaming.Frame(
            self,
            pygame.Rect(0, 0, *self.config.dimension),
            menu_bg,
            menu_bg,
            continue_animation = True,
        )
        self.pointer = Selector(self.background_frame)
        self.labels = [
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((255, 0, 000, 0), 400, 30), font, self.texts.get('LOC_JOIN_ONLINE'    ), X_POINTER[0], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((0, 255, 000, 0), 400, 30), font, self.texts.get('LOC_PLAY_OFFLINE'   ), X_POINTER[1], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((0, 000, 255, 0), 400, 30), font, self.texts.get('LOC_CREATE_ONLINE'  ), X_POINTER[2], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((255, 255, 0, 0), 400, 30), font, self.texts.get('LOC_MENU_HIGHSCORES'), X_POINTER[3], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((0, 255, 255, 0), 400, 30), font, self.texts.get('LOC_MENU_STORE'     ), X_POINTER[4], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self.background_frame, pygaming.ColoredRectangle((255, 0, 255, 0), 400, 30), font, self.texts.get('LOC_MENU_QUIT'      ), X_POINTER[5], Y_LABEL, pygaming.CENTER, 1)
        ]

        for label in self.labels[1:]:
            label.hide()

    def start(self):
        pass

    def update(self, loop_duration: int):

        actions = self.keyboard.get_actions_down()
        if actions['right'] and self.pointer_position <= 4:
            self.labels[self.pointer_position].hide()
            self.pointer_position += 1
            self.pointer.move(X_POINTER[self.pointer_position], Y_POINTER)
            self.pointer.time = 0
            self.labels[self.pointer_position].show()
        
        if actions['left'] and self.pointer_position > 0:
            self.labels[self.pointer_position].hide()
            self.pointer_position -= 1
            self.pointer.move(X_POINTER[self.pointer_position], Y_POINTER)
            self.pointer.time = 0
            self.labels[self.pointer_position].show()
        
        if actions['return']:
            self.next_phase = NEXT_PHASES[self.pointer_position]

    def next(self):
        return self.next_phase

    def end(self):
        """"""

    def apply_transition(self, next_phase: str):
        pass

g = pygaming.Game("menu", False)
MenuGamePhase(g)
g.run()