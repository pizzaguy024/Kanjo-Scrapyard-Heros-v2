import random
from database import connect
from systems.energy_system import spend_energy
from systems.world_event_system import get_today_world_event
from systems.achievement_system import unlock_achievement, check_progress_achievements

AI_RACERS = [
    {"name": "Kaito", "car": "Civic EG", "rating": 230},
    {"name": "Zero", "car": "AE86", "rating": 260},
    {"name": "Redline", "car": "Silvia S13", "rating": 300},
    {"name": "Ghost", "car": "RX-7 FC", "rating": 340},
]


def race_ai(username):
    energy_ok, message = spend_energy(username, 1)

    if not energy_ok:
        return f"""
⚡ Race denied.

{message}
"""

    event = get_today_world_event()

    db = connect()
    cur = db.cursor()

    car = cur.execute("""
        SELECT horsepower, handling, grip, reliability, condition, oil, tires, engine_wear
        FROM cars
        WHERE owner = ? AND is_active = 1
    """, (username,)).fetchone()

    player = cur.execute("""
        SELECT garage_level
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not car or not player:
        db.close()
        return "No active car found."

    garage_level = player[0]
    ai = random.choice(AI_RACERS)

    horsepower, handling, grip, reliability, condition, oil, tires, engine_wear = car

    adjusted_grip = grip + event["grip_modifier"]

    player_score = (
        horsepower
        + handling
        + adjusted_grip
        + reliability
        + random.randint(-40, 40)
        - (100 - condition)
        - (100 - oil)
        - (100 - tires)
        - engine_wear
    )

    ai_score = ai["rating"] + random.randint(-35, 35)

    wear_bonus = event["wear_modifier"]

    tire_loss = random.randint(3, 8) + wear_bonus
    oil_loss = random.randint(2, 6) + wear_bonus
    engine_damage = random.randint(1, 4) + wear_bonus
    condition_loss = random.randint(2, 6) + wear_bonus

    cur.execute("""
        UPDATE cars
        SET tires = MAX(tires - ?, 0),
            oil = MAX(oil - ?, 0),
            engine_wear = engine_wear + ?,
            condition = MAX(condition - ?, 0)
        WHERE owner = ? AND is_active = 1
    """, (tire_loss, oil_loss, engine_damage, condition_loss, username))

    if player_score >= ai_score:
        base_payout = random.randint(700, 1600)
        garage_bonus = int(base_payout * ((garage_level - 1) * 0.03))
        event_bonus = int(base_payout * (event["payout_modifier"] / 100))
        payout = base_payout + garage_bonus + event_bonus

        rep_gain = random.randint(8, 22) + event["rep_modifier"]

        cur.execute("""
            UPDATE players
            SET money = money + ?,
                reputation = reputation + ?
            WHERE username = ?
        """, (payout, rep_gain, username))

        result = f"""
🏁 AI Race Result

World Event:
{event['name']}

Opponent: {ai['name']}
Opponent Car: {ai['car']}

You won.

Base Payout: ${base_payout}
Garage Bonus: +${garage_bonus}
World Event Bonus: +${event_bonus}
Total: ${payout}

Reputation: +{rep_gain}
Energy: -1

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""
    else:
        rep_gain = random.randint(2, 6) + event["rep_modifier"]

        cur.execute("""
            UPDATE players
            SET reputation = reputation + ?
            WHERE username = ?
        """, (rep_gain, username))

        result = f"""
🏁 AI Race Result

World Event:
{event['name']}

Opponent: {ai['name']}
Opponent Car: {ai['car']}

You lost.

Reputation: +{rep_gain}
Energy: -1

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""

    db.commit()
    db.close()

    result += unlock_achievement(username, "first_race")
    result += check_progress_achievements(username)

    return result
