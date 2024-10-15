-- In this file are created every tables. This sql file is the first executed at game launch.

CREATE TABLE localizations (
    position TEXT NOT NULL, --"LOC_..."
    phase_name TEXT NOT NULL, -- the name of the phase. The text is loaded only on the corresponding phase or in every phase if the phase name is "all"
    language_code TEXT, --'en_US" for us english, "fr_FR" for french, "it_IT" for italian, "es_MX" for mexican spanish etc.
    text_value TEXT NOT NULL -- The value itself
);

CREATE TABLE speeches (
    position TEXT NOT NULL UNIQUE,
    phase_name TEXT NOT NULL,
    language_code TEXT,
    sound_path TEXT NOT NULL
);

CREATE TABLE player (
    player_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    last_connexion INTEGER NOT NULL,
    money INTEGER NOT NULL DEFAULT 200
);

CREATE TABLE character (
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    weight INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    jump INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    strength INTEGER NOT NULL
);

CREATE TABLE purchase (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (character_id) REFERENCES character(character_id)
);

CREATE TABLE game_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    game TEXT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (character_id) REFERENCES character(character_id)
);

CREATE TABLE highscores (
    highscore_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    game TEXT NOT NULL,
    score INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES character(character_id)
)
