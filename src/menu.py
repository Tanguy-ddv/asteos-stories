import math

import pygaming
import pygame
from common.constants import MENU, CREATE_GAME, LOBBY, HIGHSCORES, STORE


Y_POINTER = 300
POINTER_AMPLITUDE = 100
Y_LABEL = 150
X_POINTER = [170, 395, 620, 791, 890, 1015]
NEXT_PHASES = [CREATE_GAME, CREATE_GAME, LOBBY, HIGHSCORES, STORE, pygaming.NO_NEXT]
BUILDINGS_POSITIONS = [
    (115, 250), (290, 500), (560, 690), (740, 825), (826, 960), (980, 1070)
]


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

    def update_pointer(self):
        for label in self.labels:
            label.hide()
        self.labels[self.pointer_position].show()
        self.pointer.time = 0
        self.pointer.move(X_POINTER[self.pointer_position], Y_POINTER)

    def update(self, loop_duration: int):

        actions = self.keyboard.get_actions_down()
        if actions['right'] and self.pointer_position <= 4:
            # The player use the arrows to navigate through the menu
            self.pointer_position += 1
            self.update_pointer()

        if actions['left'] and self.pointer_position > 0:
            # The player use the arrows to navigate through the menu
            self.pointer_position -= 1
            self.update_pointer()
        
        mouse_x, _ = self.mouse.get_position()
        if self.mouse.get_velocity()[0] != 0:
            for i,pos in enumerate(BUILDINGS_POSITIONS):
                if pos[0] <= mouse_x <= pos[1] and self.pointer_position != i:
                    self.pointer_position = i
                    self.update_pointer()




        
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