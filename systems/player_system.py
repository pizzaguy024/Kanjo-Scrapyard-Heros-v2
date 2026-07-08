from datetime import date
from database import connect
from config import STARTING_MONEY, STARTING_REP, STARTING_GARAGE_LEVEL, STARTING_ENERGY
from data.cars import get_random_starter_car
from systems.energy_system import reset_energy_if_needed
from systems.rank_system import format_rank_progress
from systems.achievement_system import unlock_achievement, check_progress_achievements


def is_buster(username):
    return username.strip().upper() == "BUSTER"


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

    if is_buster(username):
        money = 20000
        reputation = 10000
        garage_level = 3
        energy = 14
        max_energy = 14

        car = {
            "name": "1995 Mitsubishi Eclipse GS",
            "rarity": "Hidden",
            "horsepower": 325,
            "handling": 82,
            "grip": 78,
            "reliability": 72,
            "condition": 100,
            "oil": 100,
            "tires": 100,
            "engine_wear": 0,
            "upgrade_level": 5,
        }
    else:
        money = STARTING_MONEY
        reputation = STARTING_REP
        garage_level = STARTING_GARAGE_LEVEL
        energy = STARTING_ENERGY
        max_energy = STARTING_ENERGY

        starter = get_random_starter_car()

        car = {
            "name": starter["name"],
            "rarity": starter["rarity"],
            "horsepower": starter["horsepower"],
            "handling": starter["handling"],
            "grip": starter["grip"],
            "reliability": starter["reliability"],
            "condition": 75,
            "oil": 100,
            "tires": 100,
            "engine_wear": 0,
            "upgrade_level": 0,
        }

    cur.execute("""
        INSERT INTO players (
            username, money, reputation, garage_level,
            energy, max_energy, last_energy_reset,
            last_daily_reward, login_streak
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        money,
        reputation,
        garage_level,
        energy,
        max_energy,
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
        car["condition"],
        car["oil"],
        car["tires"],
        car["engine_wear"],
        car["upgrade_level"],
        1,
    ))

    db.commit()
    db.close()

    achievement_text = unlock_achievement(username, "first_steps")

    if is_buster(username):
        return f"""
🌙 Hidden Driver Activated

Driver:
BUSTER

Starter Car:
1995 Mitsubishi Eclipse GS
Rarity: Hidden

Money: $20,000
Reputation: 10,000
Garage Level: 3
Energy: 14/14

The streets already know this name.
{achievement_text}
"""

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
{achievement_text}
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
    achievement_text = check_progress_achievements(username)

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
{achievement_text}
"""
