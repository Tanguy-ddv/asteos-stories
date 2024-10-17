import pygaming
import pygame
import time

from pygaming.screen.element import TOP_LEFT

from common.constants import STORE, MENU
from player import MenuPlayer
from character import MenuCharacter

class CharacterToSelectFrame(pygaming.Actor):

    def __init__(self, master: pygaming.Frame, x: int, y: int, character: MenuCharacter) -> None:
        bg = pygaming.ColoredRectangle((255, 255, 255, 0), 108, 90, 0, 0)
        bg.blit(pygaming.ColoredRectangle((255, 255, 255, 255), 98, 80, 0, 4), (5, 5))
        x_head = (108 - character.head.get_width())//2
        y_head = (90 - character.head.get_height()) - 10
        self.locked = character.locked
        bg.blit(character.head, (x_head, y_head))
        if character.locked:
            bg = pygame.transform.grayscale(bg)

        super().__init__(master, bg, x, y, TOP_LEFT, 1)
        fbg = bg.copy()
        fbg.blit(pygaming.ColoredRectangle((255, 0, 0, 255), 98, 80, 2, 4), (5, 5))
        self.focused_surface = fbg
        self.can_be_focused = True
    
    def get_surface(self) -> pygame.Surface:
        if self.focused:
            return self.focused_surface
        else:
            return self.main_surface.get()
    
    def update(self, loop_duration: int):
        pass

class SelectorFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, window: pygame.Rect) -> None:
        background = pygaming.ImageFile("menu_background.png").get().subsurface(window)
        super().__init__(master, window, background, None, None, 1, False)
        self.selected_index = 0
        self.char_frames: list[CharacterToSelectFrame] = []
        self.quit_asked = False
        font = pygaming.FontFile("Super Unicorn.ttf").get(28, (0, 0, 0, 0), self.game.settings)
        pygaming.TextButton(self, 0, 0, pygaming.ColoredRectangle((0, 0, 0, 0), 30, 30), font, 'LOC_QUIT', command=self.quit)
        print(self.children)

    def quit(self):
        self.quit_asked = True
    
    def set_characters(self, characters: list[MenuCharacter]):
        self.char_frames.clear()
        for i, character in enumerate(sorted(characters, key=lambda char: char.id_)):
            row = i%6
            col = i//6
            self.char_frames.append(CharacterToSelectFrame(self, row*108 + 50, col*90 + 50, character))
        self.char_frames[0].focus()

    def switch_char(self):
        for char_frame in self.char_frames:
            char_frame.unfocus()
        self.char_frames[self.selected_index].focus()
        self.master.switch_char()

    def update(self, loop_duration: int):
        pygaming.Frame.update(self, loop_duration)
        actions = self.game.keyboard.get_actions_down()
        if actions['right'] and self.selected_index%6 != 5:
            self.selected_index += 1
            self.switch_char()
        elif actions['left'] and self.selected_index%6 != 0:
            self.selected_index -= 1
            self.switch_char()
        elif actions['up'] and self.selected_index > 5:
            self.selected_index -= 6
            self.switch_char()
        elif actions['down'] and self.selected_index < 18:
            self.selected_index += 6
            self.switch_char()
        elif self.game.mouse.is_moving() and not self.master.confirm_frame.visible:
            mouse_x, mouse_y = self.game.mouse.get_position()
            for i, char_frame in enumerate(self.char_frames):
                if char_frame.absolute_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_index = i
                    self.switch_char()

class SelectedCharacterFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, character: MenuCharacter) -> None:

        background = pygaming.ColoredRectangle((255, 255, 255, 255), 400, 800)
        background.blit(pygaming.ColoredRectangle((120, 120, 120, 255), 200, 100), (100, 700))
        background.blit(character.std_right, (150, 450))
        stat_colored_rect = pygaming.ColoredRectangle(character.color, 25, 80)
        self.master = master
        font = pygaming.FontFile('Super Unicorn.ttf').get(25, character.color, self.game.settings)

        super().__init__(master, pygame.Rect(800, 0, 400, 800), background, None, None, 1, False)

        # Blit the strength On the top right
        StatFrame(self, pygame.Rect(50, 100, 150, 100), stat_colored_rect, font, character.strength, True, 'LOC_STRENGTH')
        StatFrame(self, pygame.Rect(50, 300, 150, 100), stat_colored_rect, font, character.mana, True, 'LOC_MANA')
        StatFrame(self, pygame.Rect(200, 100, 150, 100), stat_colored_rect, font, character.jump, False, 'LOC_JUMP')
        StatFrame(self, pygame.Rect(200, 300, 150, 100), stat_colored_rect, font, character.speed, False, 'LOC_SPEED')

        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 200, 50), font, character.name, 200, 50, anchor = pygaming.CENTER)

class StatFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, window: pygame.Rect, stat_colored_rect: pygame.Surface, font, number, from_left: bool, loc: str) -> None:
        bg = pygaming.ColoredRectangle((200, 200, 200, 255), window.width, window.height)
        if from_left:
            for i in range(number):
                bg.blit(stat_colored_rect, (0 + i*(stat_colored_rect.get_width()+5), 20 ))
        else:
            for i in range(number):
                bg.blit(stat_colored_rect, (window.width - i*(stat_colored_rect.get_width()+5) - stat_colored_rect.get_width(), 20))
        super().__init__(master, window, bg, None, None, 1, False)
        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), window.width, 20), font, loc, 0, 0)

class ConfirmFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame) -> None:
        bg = pygaming.ColoredRectangle((255, 255, 255, 255), 300, 300, 0, 10)
        bg.blit(pygaming.ColoredRectangle((0, 0, 0, 255), 300, 300, 5, 10), (0, 0))
        fbg = pygaming.ColoredRectangle((255, 255, 255, 255), 300, 300, 0, 10)
        fbg.blit(pygaming.ColoredRectangle((100, 255, 0, 255), 300, 300, 5, 10), (0,0))
        super().__init__(master, pygame.Rect(450, 250, 300, 300), bg, fbg, None, 2, True)
        lfont = pygaming.FontFile("Super Unicorn.ttf").get(20, 'black', self.game.settings)
        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 300, 100), lfont, 'LOC_VALIDATE_PURCHASE', 0, 0)
        bfont = pygaming.FontFile("Super Unicorn.ttf").get(20, 'white', self.game.settings)
        self.b1 = pygaming.TextButton(self, 40, 150, pygaming.ColoredRectangle((0, 150, 0, 255), 100, 100), bfont, 'LOC_YES', command=self.master.validate_purchase)
        pygaming.TextButton(self, 300 - 40 - 100, 150, pygaming.ColoredRectangle((200, 0, 0, 255), 100, 100), bfont, 'LOC_NO', command=lambda:(self.hide(), self.b1.unfocus()))
        self.b1.show()

class MoneyFrame(pygaming.Frame):

    def __init__(self, master: pygaming.GamePhase, window: pygame.Rect) -> None:
        super().__init__(master, window, pygaming.ColoredRectangle((255, 255, 240, 255), 200, 30), layer=2)
        font = pygaming.FontFile("Super Unicorn.ttf").get(29, 'black', self.game.settings)
        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 150, 30), font, 'LOC_MONEY', 0, 0, justify=pygaming.CENTER_LEFT)
        self.money_label = pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 50, 30), font, '0', 150, 0, justify=pygaming.CENTER_RIGHT)

class StorePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(STORE, game)
        self.player = None
        self.confirm_frame = ConfirmFrame(self)
        self.confirm_frame.hide()
        self.selector_frame = SelectorFrame(self, pygame.Rect(0, 0, 800, 800))
        self.money_frame = MoneyFrame(self, pygame.Rect(900, 700, 200, 30))

        self.selected_character_frames: list[SelectedCharacterFrame] = []
        self.characters: list[MenuCharacter] = []
    
    def validate_purchase(self):
        char_id = self.selector_frame.selected_index
        self.purchase(char_id)
        self.confirm_frame.hide()
    
    def purchase(self, character_id: int):
        if self.player.money >= 50:
            self.player.money -= 50
            self.database.execute_insert_query(
                f"""INSERT INTO purchase (player_id, character_id, time, price) VALUES 
                ({self.player.id}, {character_id+1}, {int(time.time()*1000)}, 50)"""
                )
            self.database.execute_modify_query(
                f"UPDATE player SET money = {self.player.money} WHERE player_id = {self.player.id}"
            )
            self.characters[character_id].locked = False
            x, y = self.selector_frame.char_frames[character_id].relative_coordinate
            self.selector_frame.char_frames[character_id] = CharacterToSelectFrame(self.selector_frame, x, y, self.characters[character_id])
            self.selector_frame.char_frames[character_id].focus()
            self.money_frame.money_label.set_localization_or_text(self.player.money)

    def next(self):
        if self.selector_frame.quit_asked:
            return MENU
        else:
            return pygaming.STAY

    def start(self, player: MenuPlayer):
        self.player = player
        ids = [id_[0] for id_ in self.database.execute_select_query("SELECT character_id FROM character")[0]]
        self.characters = [MenuCharacter(id_, self.database, self.player.id) for id_ in ids]
        self.selector_frame.set_characters(self.characters)

        for char in self.characters:
            self.selected_character_frames.append(SelectedCharacterFrame(self, char))
        for frame in self.selected_character_frames[1:]:
            frame.hide()
        self.money_frame.money_label.set_localization_or_text(self.player.money)

    def apply_transition(self, next_phase: str):
        return {'player' : self.player}
    
    def end(self):
        self.selector_frame.quit_asked = False

    def update(self, loop_duration):
        actions = self.keyboard.get_actions_down()
        if actions['return']:
            if self.characters[self.selector_frame.selected_index].locked and self.player.money >= 50:
                self.confirm_frame.show()
                
        ck1 = self.mouse.get_click(1)
        if ck1 is not None and ck1.duration == 0:
            for i, char_frame in enumerate(self.selector_frame.char_frames):
                if char_frame.absolute_rect.collidepoint(ck1.x, ck1.y):
                    if self.characters[i].locked and self.player.money >= 50:
                        self.selector_frame.selected_index = i
                        self.confirm_frame.show()
                        self.confirm_frame.b1.focus()
                    break
        
    def switch_char(self):
        index = self.selector_frame.selected_index
        for frame in self.selected_character_frames:
            frame.hide()
        self.selected_character_frames[index].show()
