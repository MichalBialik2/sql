import sqlite3
from dataclasses import dataclass

DB_NAME = "szkola.db"

@dataclass
class Szkola:
    id: int
    nazwa: str

@dataclass
class Ranking:
    id: int
    szkola_id: int
    pozycja: int

@dataclass
class Nauczyciel:
    id: int
    szkola_id: int
    imie: str
    nazwisko: str

@dataclass
class Klasa:
    id: int
    szkola_id: int
    nazwa: str
    profil_id: int | None

@dataclass
class ProfilKlasy:
    id: int
    nazwa: str

@dataclass
class Uczen:
    id: int
    szkola_id: int
    imie: str
    nazwisko: str
    klasa_id: int | None

@dataclass
class Legitymacja:
    id: int
    uczen_id: int
    aktualna: bool

@dataclass
class Srednia:
    id: int
    uczen_id: int
    wartosc: float

@dataclass
class Przedmiot:
    id: int
    nazwa: str

@dataclass
class Ocena:
    id: int
    uczen_id: int
    przedmiot_id: int
    wartosc: float | None = None

class BazaDanych:
    def __init__(self, nazwa_pliku: str = DB_NAME):
        self.nazwa_pliku = nazwa_pliku
        self._utworz_tabele()

    def _polaczenie(self):
        conn = sqlite3.connect(self.nazwa_pliku)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _utworz_tabele(self):
        schema = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS szkola (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    szkola_id INTEGER NOT NULL,
    pozycja INTEGER NOT NULL,
    FOREIGN KEY (szkola_id)
        REFERENCES szkola(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_ranking_szkola ON ranking(szkola_id);

CREATE TABLE IF NOT EXISTS nauczyciel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    szkola_id INTEGER NOT NULL,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    FOREIGN KEY (szkola_id)
        REFERENCES szkola(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_nauczyciel_szkola ON nauczyciel(szkola_id);

CREATE TABLE IF NOT EXISTS profil_klasy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS klasa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    szkola_id INTEGER NOT NULL,
    nazwa TEXT NOT NULL,
    profil_id INTEGER,
    FOREIGN KEY (szkola_id)
        REFERENCES szkola(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (profil_id)
        REFERENCES profil_klasy(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_klasa_szkola ON klasa(szkola_id);
CREATE INDEX IF NOT EXISTS idx_klasa_profil ON klasa(profil_id);

CREATE TABLE IF NOT EXISTS uczen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    szkola_id INTEGER NOT NULL,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    klasa_id INTEGER,
    FOREIGN KEY (szkola_id)
        REFERENCES szkola(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (klasa_id)
        REFERENCES klasa(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_uczen_szkola ON uczen(szkola_id);
CREATE INDEX IF NOT EXISTS idx_uczen_klasa ON uczen(klasa_id);

CREATE TABLE IF NOT EXISTS legitymacja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uczen_id INTEGER NOT NULL UNIQUE,
    aktualna INTEGER NOT NULL DEFAULT 1,
    numer TEXT,
    FOREIGN KEY (uczen_id)
        REFERENCES uczen(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_legitymacja_uczen ON legitymacja(uczen_id);

CREATE TABLE IF NOT EXISTS srednia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uczen_id INTEGER NOT NULL UNIQUE,
    wartosc REAL NOT NULL,
    FOREIGN KEY (uczen_id)
        REFERENCES uczen(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_srednia_uczen ON srednia(uczen_id);

CREATE TABLE IF NOT EXISTS przedmiot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ocena (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uczen_id INTEGER NOT NULL,
    przedmiot_id INTEGER NOT NULL,
    wartosc REAL NOT NULL,
    FOREIGN KEY (uczen_id)
        REFERENCES uczen(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (przedmiot_id)
        REFERENCES przedmiot(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_ocena_uczen ON ocena(uczen_id);
CREATE INDEX IF NOT EXISTS idx_ocena_przedmiot ON ocena(przedmiot_id);
"""


        with self._polaczenie() as conn:
            conn.executescript(schema)

    def dodaj_szkołe(self, nazwa: str) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO szkola (nazwa) VALUES (?)", (nazwa,))
            return cur.lastrowid

    def dodaj_ranking(self, szkola_id: int, pozycja: int) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO ranking (szkola_id, pozycja) VALUES (?, ?)", (szkola_id, pozycja))
            return cur.lastrowid

    def dodaj_nauczyciela(self, szkola_id: int, imie: str, nazwisko: str) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO nauczyciel (szkola_id, imie, nazwisko) VALUES (?, ?, ?)", (szkola_id, imie, nazwisko))
            return cur.lastrowid
        
    def dodaj_profil(self, nazwa: str) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO profil_klasy (nazwa) VALUES (?)", (nazwa,))
            return cur.lastrowid
        
    def dodaj_klase(self, szkola_id: int, nazwa: str, profil_id: int | None = None) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO klasa (szkola_id, nazwa, profil_id) VALUES (?, ?, ?)", (szkola_id, nazwa, profil_id))
            return cur.lastrowid


    def dodaj_ucznia(self, szkola_id: int, imie: str, nazwisko: str, klasa_id: int | None = None) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO uczen (szkola_id, imie, nazwisko, klasa_id) VALUES (?, ?, ?, ?)", (szkola_id, imie, nazwisko, klasa_id))
            return cur.lastrowid

    def usun_ucznia(self, uczen_id: int) -> None:
        with self._polaczenie() as conn:
            conn.execute("DELETE FROM uczen WHERE id = ?", (uczen_id,))

    def dodaj_legitymacje(self, uczen_id: int, aktualna: bool = True, numer: str | None = None) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO legitymacja (uczen_id, aktualna, numer) VALUES (?, ?, ?)", (uczen_id, int(aktualna), numer))
            return cur.lastrowid
        
    def dodaj_srednia(self, uczen_id: int, wartosc: float) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO srednia (uczen_id, wartosc) VALUES (?, ?)", (uczen_id, wartosc))
            return cur.lastrowid


    def dodaj_przedmiot(self, nazwa: str) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO przedmiot (nazwa) VALUES (?)", (nazwa,))
            return cur.lastrowid

    def dodaj_ocene(self, uczen_id: int, przedmiot_id: int, wartosc: float | None = None) -> int:
        with self._polaczenie() as conn:
            cur = conn.execute("INSERT INTO ocena (uczen_id, przedmiot_id, wartosc) VALUES (?, ?, ?)", (uczen_id, przedmiot_id, wartosc))
            return cur.lastrowid



db = BazaDanych()
s1 = db.dodaj_szkołe("47 LO")
p1 = db.dodaj_profil("Mat-inf")
k1 = db.dodaj_klase("47 LO", "1A", "Mat-inf")
uc1 = db.dodaj_ucznia("47 LO", "Kasia", "Kowalska", k1)
db.dodaj_przedmiot("Matematyka")
db.dodaj_przedmiot("Informatyka")
db.dodaj_przedmiot("Polski")
db.dodaj_przedmiot("Fizyka")

