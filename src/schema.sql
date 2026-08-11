DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS guiche;
DROP TABLE IF EXISTS senha;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE guiche (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL
);

CREATE TABLE senha (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    numero INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (
    status IN ('aguardando', 'atendendo', 'finalizada')
    ),
    guiche INTEGER,
    horario DATETIME NOT NULL,

    FOREIGN KEY (guiche) REFERENCES guiche(id)

);