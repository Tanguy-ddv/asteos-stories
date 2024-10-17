import pygaming
import pygame
import time

from pygaming.screen.element import TOP_LEFT

from common.constants import STORE, MENU
from player import MenuPlayer
from character import MenuCharacter, CharacterFolder

class CharacterToSelectFrame(pygaming.Actor):

    def __init__(self, master: pygaming.Frame, x: int, y: int, character: MenuCharacter) -> None:
        bg = pygaming.ColoredRectangle((255, 255, 255, 0), 108, 90, 0, 0)
        bg.blit(pygaming.ColoredRectangle((255, 255, 255, 255), 98, 80, 0, 4), (10, 5))
        x_head = (108 - character.head.get_width())//2
        y_head = (90 - character.head.get_height())
        self.locked = character.locked
        bg.blit(character.head, (x_head, y_head))
        if character.locked:
            bg = pygame.transform.grayscale(bg)

        super().__init__(master, bg, x, y, TOP_LEFT, 1)
        bg.blit(pygaming.ColoredRectangle((255, 0, 0, 255), 98, 80, 2, 4), 0, 0)
        self.focused_surface = bg
        self.can_be_focused = True
    
    def get_surface(self) -> pygame.Surface:
        if self.focused:
            return self.focused_surface
        else:
            return self.main_surface
    
    def update(self, loop_duration: int):
        pass

class SelectorFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, window: pygame.Rect) -> None:
        background = pygaming.ImageFile("menu_background").get().subsurface(window)
        super().__init__(master, window, background, None, None, 1, False)
        self.selected_index = 0
        self.char_frames: list[CharacterToSelectFrame] = []
    
    def set_characters(self, characters: list[MenuCharacter]):
        self.char_frames.clear()
        for i, character in enumerate(sorted(characters, key=lambda char: char.id_)):
            row = i//4
            col = i%4
            self.char_frames.append(CharacterToSelectFrame(self, row*108 + 50, col*90 + 50, character))
        self.char_frames[0].focus()

    def switch_char(self):
        for char_frame in self.char_frames:
            char_frame.unfocus()
        self.char_frames[self.selected_index].focus()

    def update(self, loop_duration: int):
        actions = self.game.keyboard.get_actions_down()
        if actions['right'] and self.selected_index%4 != 3:
            self.selected_index += 1
            self.switch_char()
        elif actions['left'] and self.selected_index%4 != 0:
            self.selected_index -= 1
            self.switch_char()
        elif actions['up'] and self.selected_index > 3:
            self.selected_index -= 4
            self.switch_char()
        elif actions['down'] and self.selected_index < 20:
            self.selected_index += 4
            self.switch_char()
        else:
            mouse_x, mouse_y = self.game.mouse.get_position()
            for i, char_frame in enumerate(self.char_frames):
                if char_frame.absolute_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_index = i
                    self.switch_char()

class SelectedCharacterFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, character: MenuCharacter) -> None:

        background = pygaming.ColoredRectangle((255, 255, 255, 255), 400, 800)
        background.blit(pygaming.ColoredRectangle((120, 120, 120, 255), 200, 100), (100, 700))
        background.blit(character.std_right, (200 - 54, 700 - 108))
        # Blit strength, mana, speed and jump symbols with value represented with colored rectangles
        # (Red for 1, orange for 2, yellow for 3, yellow-green for 4 and green for 5)
        super().__init__(master, pygame.Rect(800, 0, 400, 800), background, None, None, 1, False)

class ConfirmFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame) -> None:
        bg = pygaming.ColoredRectangle((255, 255, 255, 255), 300, 300, 0, 10)
        bg.blit(pygaming.ColoredRectangle((0, 0, 0, 255), 300, 300, 5, 10))
        fbg = pygaming.ColoredRectangle((255, 255, 255, 255), 300, 300, 0, 10)
        fbg.blit(pygaming.ColoredRectangle((100, 255, 0, 255), 300, 300, 5, 10))
        super().__init__(master, pygame.Rect(450, 250, 300, 300), bg, fbg, None, 2, True)
        lfont = pygaming.FontFile("Super Unicorn.ttf").get(20, 'black', self.game.settings)
        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 300, 100), lfont, 'LOC_VALIDATE_PURCHASE', 0, 0)
        bfont = pygaming.FontFile("Super Unicorn.ttf").get(20, 'white', self.game.settings)
        self.b1 = pygaming.TextButton(self, 40, 150, pygaming.ColoredRectangle((0, 150, 0, 255), 100, 100), bfont, 'LOC_YES', command=self.master.validate_purchase)
        pygaming.TextButton(self, 40, 150, pygaming.ColoredRectangle((200, 0, 0, 255), 100, 100), bfont, 'LOC_NO', command=lambda:(self.hide(), self.b1.unfocus()))


class StorePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(STORE, game)
        self.player = None
        self.selector_frame = SelectorFrame(self, pygame.Rect(0, 0, 800, 800))
        self.confirm_frame = ConfirmFrame(self)
        self.selected_character_frames: list[SelectedCharacterFrame] = []
    
    def validate_purchase(self):
        char_id = self.selector_frame.selected_index
        self.purchase(char_id)
    
    def purchase(self, character_id):
        if self.player.money >= 50:
            self.player.money -= 50
            self.database.execute_insert_query(
                f"""INSERT INTO purchase (player_id, character_id, time, price) VALUES 
                ({self.player.id}, {character_id}, {int(time.time()*1000)}, 50)"""
                )
            self.database.execute_modify_query(
                f"UPDATE player SET money = {self.player.money} WHERE player_id = {self.player.id};"
            )

    def start(self, player: MenuPlayer):
        self.player = player
        ids = [id_[0] for id_ in self.database.execute_select_query("SELECT character_id FROM character")]
        characters = [MenuCharacter(id_, self.database, self.player.id) for id_ in ids]
        self.selector_frame.set_characters(characters)

        for char in characters:
            self.selected_character_frames.append(SelectedCharacterFrame(self, char))

    def apply_transition(self, next_phase: str):
        return {'player' : self.player}
    
    def end(self):
        pass

    def update(self, loop_duration):
        actions = self.keyboard.get_actions_down()
        if actions['enter']:
            self.confirm_frame.show()
            self.confirm_frame.b1.focus()
        ck1 = self.mouse.get_click(1)
        if ck1 is not None and ck1.duration == 0:
            for i, char_frame in enumerate(self.selector_frame.char_frames):
                if char_frame.absolute_rect.collidepoint(ck1.x, ck1.y):
                    self.selector_frame.selected_index = i
                    self.confirm_frame.show()
                    self.confirm_frame.b1.focus()
