DROP TABLE IF EXISTS users;
CREATE TABLE users (
	uid SERIAL PRIMARY KEY,
	email VARCHAR(60) NOT NULL UNIQUE,
	passwordhash VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS words;
CREATE TABLE words (
	wid SERIAL PRIMARY KEY,
	english VARCHAR(60) NOT NULL,
	chinese VARCHAR(60) NOT NULL,
	pinyin VARCHAR(60)
);

DROP TABLE IF EXISTS decks;
CREATE TABLE decks (
	did SERIAL PRIMARY KEY,
	uid INTEGER REFERENCES users(uid),
	name VARCHAR(60) NOT NULL
);

DROP TABLE IF EXISTS deckwords;
CREATE TABLE deckwords (
	dwid SERIAL PRIMARY KEY,
	did INTEGER REFERENCES decks(did),
	wid INTEGER REFERENCES words(wid)
);