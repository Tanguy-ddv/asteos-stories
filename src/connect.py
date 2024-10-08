import pygaming
import pygame
from player import MenuPlayer
from common.constants import MENU
import time

class ConnectFrame(pygaming.Frame):

    def __init__(self, master: pygaming.GamePhase) -> None:
        super().__init__(master,
            pygame.Rect(0, 0, *master.config.dimension),
            pygaming.ImageFile("menu_background.png").get(),
            None,
            continue_animation = True
        )

        existing_players = self.master.database.execute_select_query("SELECT player_id, name, money, last_connexion FROM player")[0]
        self.players: list[MenuPlayer] = sorted([MenuPlayer(*player) for player in existing_players], key=lambda player: player.last_connexion, reverse=True)
        font = pygaming.FontFile("Super Unicorn.ttf").get(30, (0, 0, 0, 255), self.master.settings)
        # Log in part
        pygaming.Label(self, pygaming.ColoredRectangle((255, 255, 255, 0), 400, 50), font, 'LOC_CONNECT', 300, 200, pygaming.CENTER)
        self.labels = [
            pygaming.Label(self, pygaming.ColoredRectangle((255, 255, 255, 255), 400, 50), font, player.name, 300, 250, pygaming.CENTER)
            for player in self.players
        ]
        for label in self.labels[1:]:
            label.hide()
        
        # Sign in part
        pygaming.Label(self, pygaming.ColoredRectangle((255, 255, 255, 0), 400, 50), font, 'LOC_CREATE_PROFILE', 900, 200, pygaming.CENTER, blinking_period=1500)
        self.entry = pygaming.Entry(
            self,
            900,
            250,
            pygaming.ColoredRectangle((255, 255, 255, 255), 400, 50),
            font,
            anchor=pygaming.CENTER,
            max_length=20,
            extra_characters="àéèùç",
            forbid_characters="()[],;./:!?*$"
        )
    
        self.validate_button = pygaming.TextButton(
            self,
            600,
            350,
            pygaming.ColoredRectangle((255, 255, 255, 255), 300, 100),
            font,
            'LOC_LETS_PLAY',
            anchor=pygaming.CENTER,
            command=master.set_ready
        )

    def update_selector(self, player_index: int):
        for label in self.labels:
            label.hide()
        self.labels[player_index].show()


class Connect(pygaming.GamePhase):
    
    def __init__(self, game: pygaming.Game) -> None:
        super().__init__("connect", game)

        self.frame = ConnectFrame(self)
        self.player_index = 0
        self.ready = False

    def set_ready(self):
        self.ready = True
    
    def start(self):
        pass

    def update(self, loop_duration: int):
        
        actions = self.keyboard.get_actions_down()

        if actions['right'] and self.player_index < len(self.frame.players) - 1:
            self.player_index += 1
            self.frame.update_selector(self.player_index)
        
        if actions['left'] and self.player_index > 0:
            self.player_index -= 1
            self.frame.update_selector(self.player_index)

    def next(self):
        return MENU if self.ready else pygaming.STAY

    def apply_transition(self, next_phase: str):
        player_name = self.frame.entry.get()
        last_connexion = int(time.time())
        if player_name:
            
            self.database.execute_insert_query(
                f"INSERT INTO player (name, money, last_connexion) VALUES ('{player_name}', {150}, {last_connexion})")
            return {'player' : MenuPlayer(len(self.frame.players), player_name, 150, last_connexion)}

        else:
            player = self.frame.players[self.player_index]
            player.last_connexion = last_connexion
            self.database.execute_modify_query(f"UPDATE player SET last_connexion = {last_connexion} WHERE player_id = {player.id}")
        return {'player' : player}

    def end(self):
        # Update the player last connection or store him into the database
        pass