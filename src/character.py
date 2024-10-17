import pygaming
import pygame
from common.constants import MENU, HIGHSCORES, GAME

class CharacterFolder(pygaming.DataFile):

    def __init__(self, path: str) -> None:
        super().__init__('characters/' + path, True)

    def get(self, kind: str):
        if kind == MENU:
            std = pygame.image.load(self.full_path + 'stand.png')
            std = pygame.transform.scale(std, (std.get_width()*2, std.get_height()*2))
            return std, pygame.transform.flip(std, 1, 0), pygame.image.load(self.full_path + 'lobby_head.png')

        elif kind == HIGHSCORES:
            return pygame.image.load(self.full_path + 'small_head.png')
    
        else:
            return 

class MenuCharacter:

    def __init__(self,
        id_: int,
        database: pygaming.Database,
        player_id: int
    ):
        self.id_ = id_
        output, _desc = database.execute_select_query(
            f"SELECT * FROM character WHERE character_id = {id_}"
        )
        _id, self.name, path, _weight, self.speed, self.jump, self.mana, self.strength, red, green, blue = output[0]
        self.color = (red, green, blue)
        self.std_left, self.std_right, self.head = CharacterFolder(path).get(MENU)
        self.locked = (database.execute_select_query(
            f"SELECT COUNT(*) FROM purchase WHERE player_id = {player_id} AND character_id = {id_}"
        )[0][0][0] == 0)
