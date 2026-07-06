import sqlite3

DB_NAME = "kanjo_v2.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        money INTEGER NOT NULL,
        reputation INTEGER NOT NULL,
        garage_level INTEGER NOT NULL,
        energy INTEGER NOT NULL,
        max_energy INTEGER NOT NULL,
        last_energy_reset TEXT,
        last_daily_reward TEXT,
        login_streak INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        name TEXT NOT NULL,
        rarity TEXT NOT NULL,
        horsepower INTEGER NOT NULL,
        handling INTEGER NOT NULL,
        grip INTEGER NOT NULL,
        reliability INTEGER NOT NULL,
        condition INTEGER NOT NULL,
        oil INTEGER NOT NULL,
        tires INTEGER NOT NULL,
        engine_wear INTEGER NOT NULL,
        upgrade_level INTEGER NOT NULL,
        is_active INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS world_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_date TEXT UNIQUE,
        name TEXT,
        description TEXT,
        grip_modifier INTEGER,
        payout_modifier INTEGER,
        rep_modifier INTEGER,
        wear_modifier INTEGER
    )
    """)

    db.commit()
    db.close()
