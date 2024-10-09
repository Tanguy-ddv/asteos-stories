CREATE TABLE character(
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    weight INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    jump INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    strength INTEGER NOT NULL
);

CREATE TABLE highscores(
    highscore_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    game TEXT NOT NULL,
    score TEXT NOT NULL,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES character(character_id)
)