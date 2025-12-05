import sqlite3

DB_NAME = "szkola.db"


def polaczenie() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def utworz_tabele() -> None:
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

    with polaczenie() as conn:
        conn.executescript(schema)



def dodaj_szkole(nazwa: str) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO szkola (nazwa) VALUES (?)", (nazwa,))
        return cur.lastrowid


def dodaj_ranking(szkola_id: int, pozycja: int) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO ranking (szkola_id, pozycja) VALUES (?, ?)", (szkola_id, pozycja))
        return cur.lastrowid


def dodaj_nauczyciela(szkola_id: int, imie: str, nazwisko: str) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO nauczyciel (szkola_id, imie, nazwisko) VALUES (?, ?, ?)", (szkola_id, imie, nazwisko))
        return cur.lastrowid


def dodaj_profil(nazwa: str) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO profil_klasy (nazwa) VALUES (?)", (nazwa,))
        return cur.lastrowid


def dodaj_klase(szkola_id: int, nazwa: str, profil_id: int | None = None) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO klasa (szkola_id, nazwa, profil_id) VALUES (?, ?, ?)", (szkola_id, nazwa, profil_id))
        return cur.lastrowid


def dodaj_ucznia(szkola_id: int, imie: str, nazwisko: str, klasa_id: int | None = None) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO uczen (szkola_id, imie, nazwisko, klasa_id) VALUES (?, ?, ?, ?)", (szkola_id, imie, nazwisko, klasa_id))
        return cur.lastrowid


def dodaj_legitymacje(uczen_id: int, aktualna: bool = True, numer: str | None = None) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO legitymacja (uczen_id, aktualna, numer) VALUES (?, ?, ?)", (uczen_id, int(aktualna), numer))
        return cur.lastrowid


def dodaj_srednia(uczen_id: int, wartosc: float) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO srednia (uczen_id, wartosc) VALUES (?, ?)", (uczen_id, wartosc))
        return cur.lastrowid


def dodaj_przedmiot(nazwa: str) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO przedmiot (nazwa) VALUES (?)", (nazwa,))
        return cur.lastrowid


def dodaj_ocene(uczen_id: int, przedmiot_id: int, wartosc: float) -> int:
    with polaczenie() as conn:
        cur = conn.execute("INSERT INTO ocena (uczen_id, przedmiot_id, wartosc) VALUES (?, ?, ?)", (uczen_id, przedmiot_id, wartosc))
        return cur.lastrowid


utworz_tabele()
