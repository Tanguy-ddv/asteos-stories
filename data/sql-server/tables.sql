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