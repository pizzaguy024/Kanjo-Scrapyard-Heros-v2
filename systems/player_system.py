from datetime import date
from database import connect
from config import STARTING_MONEY, STARTING_REP, STARTING_GARAGE_LEVEL, STARTING_ENERGY
from data.cars import get_random_starter_car
from systems.energy_system import reset_energy_if_needed
from systems.rank_system import format_rank_progress


def create_player(username):
    db = connect()
    cur = db.cursor()

    existing = cur.execute("""
        SELECT username
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if existing:
        db.close()
        return "You already have a player profile."

    today = date.today().isoformat()
    car = get_random_starter_car()

    cur.execute("""
        INSERT INTO players (
            username, money, reputation, garage_level,
            energy, max_energy, last_energy_reset,
            last_daily_reward, login_streak
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        STARTING_MONEY,
        STARTING_REP,
        STARTING_GARAGE_LEVEL,
        STARTING_ENERGY,
        STARTING_ENERGY,
        today,
        None,
        0,
    ))

    cur.execute("""
        INSERT INTO cars (
            owner, name, rarity, horsepower, handling, grip, reliability,
            condition, oil, tires, engine_wear, upgrade_level, is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        car["name"],
        car["rarity"],
        car["horsepower"],
        car["handling"],
        car["grip"],
        car["reliability"],
        75,
        100,
        100,
        0,
        0,
        1,
    ))

    db.commit()
    db.close()

    return f"""
🏚️ Welcome to the Scrap Yard.

Starter Car:
{car['name']}
Rarity: {car['rarity']}

Money: ${STARTING_MONEY}
Reputation: {STARTING_REP}
Rank: Scrap Rookie
Energy: {STARTING_ENERGY}/{STARTING_ENERGY}

Every legend starts as scrap.
"""


def profile(username):
    reset_energy_if_needed(username)

    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money, reputation, garage_level, energy, max_energy, login_streak
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No profile found. Start a new player first."

    car = cur.execute("""
        SELECT name, rarity, horsepower, handling, grip, reliability, condition
        FROM cars
        WHERE owner = ? AND is_active = 1
    """, (username,)).fetchone()

    db.close()

    money, rep, garage_level, energy, max_energy, streak = player
    rank_text = format_rank_progress(rep)

    return f"""
👤 Driver: {username}

Money: ${money}
Reputation: {rep}
{rank_text}
Garage Level: {garage_level}
Energy: {energy}/{max_energy}
Login Streak: {streak}

Active Car:
{car[0]}
Rarity: {car[1]}
Horsepower: {car[2]}
Handling: {car[3]}
Grip: {car[4]}
Reliability: {car[5]}
Condition: {car[6]}%
"""
