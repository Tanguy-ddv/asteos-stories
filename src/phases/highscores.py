import pygaming
import pygame
from common.constants import HIGHSCORES, MENU
from player import MenuPlayer
from character import CharacterFolder

RECORD_HEIGHT = 55

class RecordFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, window: pygame.Rect, record: tuple[str, int, str], font: pygaming.Font, player: MenuPlayer) -> None:
        super().__init__(master, window, pygaming.ColoredRectangle((0, 0, 0, 0), 300, RECORD_HEIGHT, 2))
        pygaming.Frame(
            self,
            pygame.Rect(0, 0, 54, RECORD_HEIGHT),
            CharacterFolder(record[2]).get(HIGHSCORES),
        )
        pygaming.Label(
            self,
            pygaming.ColoredRectangle((0, 0, 0, 0), 170, RECORD_HEIGHT, 2),
            font,
            record[0],
            55,
            RECORD_HEIGHT - 5,
            anchor = pygaming.BOTTOM_LEFT,
            justify=pygaming.BOTTOM_LEFT,
            blinking_period=None if player.name != record[0] else 1000
        )
        
        pygaming.Label(
            self,
            pygaming.ColoredRectangle((0, 0, 0, 0), 100, RECORD_HEIGHT, 2),
            font,
            str(record[1]),
            295,
            RECORD_HEIGHT - 5,
            anchor=pygaming.BOTTOM_RIGHT,
            justify=pygaming.BOTTOM_RIGHT,
            blinking_period=None if player.name != record[0] else 1000)

GAME_NAME_LOCS = {
    'nut_race' : 'LOC_NUT_RACE'
}


class GameHighScoresFrame(pygaming.Frame):

    def __init__(self, master: pygaming.Frame, window: pygame.Rect, game_name:str, records: list[tuple], font : pygaming.Font, player: MenuPlayer) -> None:
        super().__init__(master, window, pygaming.ColoredRectangle((255, 255, 255, 255), 300, RECORD_HEIGHT*6+5))
        pygaming.Label(self, pygaming.ColoredRectangle((0, 0, 0, 0), 300, RECORD_HEIGHT), font, GAME_NAME_LOCS[game_name], 0, 0)
        for i,record in enumerate(records[:5]):
            RecordFrame(self, pygame.Rect(0, (i+1)*RECORD_HEIGHT, 295, RECORD_HEIGHT), record, font, player)

class HighScoresFrame(pygaming.Frame):

    def __init__(self, master: pygaming.GamePhase, highscores_dict: dict[str, list[tuple[str, str, int]]], player: MenuPlayer) -> None:
        super().__init__(master,
            pygame.Rect(0, 0, *master.config.dimension),
            pygaming.ImageFile("menu_background.png").get(),
            None,
            continue_animation = True
        )
        font = pygaming.FontFile("Super Unicorn.ttf").get(28, (0, 0, 0, 0), self.game.settings)
        for i,(game, records) in enumerate(highscores_dict.items()):
            row = i//3
            column = i%3
            GameHighScoresFrame(self, pygame.Rect(50 + row*350, 150 + 220*column, 300, RECORD_HEIGHT*6+5), game, records, font, player)
        
        self.quit_asked = False
        font = pygaming.FontFile("Super Unicorn.ttf").get(28, (0, 0, 0, 0), self.game.settings)
        pygaming.TextButton(self, 0, 0, pygaming.ColoredRectangle((0, 0, 0, 0), 30, 30), font, 'LOC_QUIT', command=self.quit)

    def quit(self):
        self.quit_asked = True

class HighScoresGamePhase(pygaming.GamePhase):

    def __init__(self, game: pygaming.Game) -> None:
        super().__init__(HIGHSCORES, game)

    def start(self, player: MenuPlayer):
        self.player = player
        highscores = self.database.execute_select_query(
            # Select the five best scores for each game from your own results and the highscore database.
            """SELECT player_name, game, score, path FROM (

                SELECT player_name, game, score, path,
                    RANK() OVER (PARTITION BY game ORDER BY score DESC) AS rank
                FROM (

            SELECT highscores.player_name, highscores.game, highscores.score, character.path
            FROM character
            JOIN highscores ON highscores.character_id = character.character_id

            UNION
                SELECT player.name AS player_name, game_results.game, game_results.score, character.path
                FROM character
                JOIN game_results ON game_results.character_id = character.character_id
                JOIN player ON game_results.player_id = player.player_id
                )
            )
            WHERE rank <= 5
            """
        )[0]
        highscores_dict = {record[1] : [] for record in highscores}
        for record in highscores:
            highscores_dict[record[1]].append((record[0], record[2], record[3]))
        
        self.frame = HighScoresFrame(self, highscores_dict, player)

    def update(self, loop_duration: int):
        pass

    def next(self):
        if self.frame.quit_asked:
            return MENU
        else:
            return pygaming.STAY
    
    def apply_transition(self, next_phase: str):
        return {'player' : self.player}

    def end(self):
        pass


