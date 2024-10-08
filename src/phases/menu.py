import math

import pygaming
import pygame
from player import MenuPlayer
from common.constants import MENU, CREATE_GAME, LOBBY, HIGHSCORES, STORE


Y_POINTER = 300
POINTER_AMPLITUDE = 100
Y_LABEL = 150
X_POINTER = [170, 395, 620, 791, 890, 1015]
NEXT_PHASES = [CREATE_GAME, CREATE_GAME, LOBBY, HIGHSCORES, STORE, pygaming.NO_NEXT]
BUILDINGS_POSITIONS = [
    (115, 250), (290, 500), (560, 690), (740, 825), (826, 960), (980, 1070)
]


class Pointer(pygaming.Actor):

    def __init__(self, master: pygaming.Frame) -> None:
        super().__init__(master, pygaming.ImageFile("menu_pointer.png").get(rotation=180), X_POINTER[0], Y_POINTER, pygaming.CENTER, 1)
        self.time = 0
        self.pulsation = 2*math.pi*0.2
    
    def update(self, loop_duration: int):
        self.time += loop_duration
        self.translate(0, self.get_speed()/loop_duration)

    def get_speed(self):
        return math.cos(self.time*self.pulsation/1000)*self.pulsation*POINTER_AMPLITUDE

    def get_surface(self) -> pygame.Surface:
        return self.main_surface.get()

class MenuChoiceFrame(pygaming.Frame):

    def __init__(self, master: pygaming.GamePhase) -> None:
        super().__init__(
            master,
            pygame.Rect(0, 0, *master.config.dimension),
            pygaming.ImageFile("menu_background.png").get(),
            None,
            continue_animation = True
        )
        font = pygaming.FontFile("Super Unicorn.ttf").get(30, (0, 0, 0, 255), self.master.settings)
        self.pointer = Pointer(self)
        self.labels = [
            pygaming.Label(self, pygaming.ColoredRectangle((255, 0, 000, 0), 400, 30), font, 'LOC_JOIN_ONLINE'    , X_POINTER[0], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self, pygaming.ColoredRectangle((0, 255, 000, 0), 400, 30), font, 'LOC_PLAY_OFFLINE'   , X_POINTER[1], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self, pygaming.ColoredRectangle((0, 000, 255, 0), 400, 30), font, 'LOC_CREATE_ONLINE'  , X_POINTER[2], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self, pygaming.ColoredRectangle((255, 255, 0, 0), 400, 30), font, 'LOC_MENU_HIGHSCORES', X_POINTER[3], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self, pygaming.ColoredRectangle((0, 255, 255, 0), 400, 30), font, 'LOC_MENU_STORE'     , X_POINTER[4], Y_LABEL, pygaming.CENTER, 1),
            pygaming.Label(self, pygaming.ColoredRectangle((255, 0, 255, 0), 400, 30), font, 'LOC_MENU_QUIT'      , X_POINTER[5], Y_LABEL, pygaming.CENTER, 1)
        ]

        for label in self.labels[1:]:
            label.hide()
        
    def update_pointer(self, pointer_index: int):
        for label in self.labels:
            label.hide()
        self.labels[pointer_index].show()
        self.pointer.time = 0
        self.pointer.move(X_POINTER[pointer_index], Y_POINTER)

class MenuGamePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(MENU, game)
        self.pointer_index = 0
        self.next_phase = pygaming.STAY
        self.choice_frame = MenuChoiceFrame(self)
        self.player = None

    def start(self, player: MenuPlayer):
        self.player = player
        self.pointer_index = 0
        self.choice_frame.update_pointer(0)

    def update(self, loop_duration: int):

        actions = self.keyboard.get_actions_down()
        if actions['right'] and self.pointer_index <= 4:
            # The player use the arrows to navigate through the menu
            self.pointer_index += 1
            self.choice_frame.update_pointer(self.pointer_index)

        if actions['left'] and self.pointer_index > 0:
            # The player use the arrows to navigate through the menu
            self.pointer_index -= 1
            self.choice_frame.update_pointer(self.pointer_index)
        
        mouse_x, _ = self.mouse.get_position()
        if self.mouse.get_velocity()[0] != 0:
            for i,pos in enumerate(BUILDINGS_POSITIONS):
                if pos[0] <= mouse_x <= pos[1] and self.pointer_index != i:
                    self.pointer_index = i
                    self.choice_frame.update_pointer(self.pointer_index)

        ck1 = self.mouse.get_click(1)
        if ck1 is not None and ck1.duration == 0:
            for i,pos in enumerate(BUILDINGS_POSITIONS):
                if pos[0] <= ck1.x <= pos[1]:
                    self.pointer_index = i
                    self.next_phase = NEXT_PHASES[self.pointer_index]
                    self.choice_frame.update_pointer(self.pointer_index)
        
        if actions['return']:
            self.next_phase = NEXT_PHASES[self.pointer_index]

    def next(self):
        return self.next_phase

    def end(self):
        """"""

    def apply_transition(self, next_phase: str):
        if next_phase == HIGHSCORES:
            return {'player' : self.player}
        if next_phase == LOBBY:
            return {'player' : self.player}
        if next_phase == CREATE_GAME:
            if self.pointer_index == 0:
                return {'online' : True, 'player': self.player}
            else:
                return {'online' : False, 'player': self.player}
        if next_phase == STORE:
            return {'player' : self.player}
