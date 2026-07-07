import random
from database import connect
from systems.energy_system import spend_energy
from systems.world_event_system import get_today_world_event
from systems.achievement_system import unlock_achievement, check_progress_achievements


BOSSES = [
    {
        "name": "Kaito",
        "title": "Scrap Yard Rookie",
        "car": "1992 Honda Civic EG",
        "required_rep": 100,
        "rating": 300,
        "payout": 2500,
        "rep_reward": 75,
    },
    {
        "name": "Redline",
        "title": "Dockside Menace",
        "car": "1991 Nissan Silvia S13",
        "required_rep": 500,
        "rating": 450,
        "payout": 6000,
        "rep_reward": 150,
    },
    {
        "name": "Ghost",
        "title": "Midnight Runner",
        "car": "1989 Mazda RX-7 FC",
        "required_rep": 1500,
        "rating": 650,
        "payout": 12000,
        "rep_reward": 300,
    },
    {
        "name": "Blackbird",
        "title": "Expressway King",
        "car": "1997 Nissan Skyline GTS-T",
        "required_rep": 5000,
        "rating": 900,
        "payout": 25000,
        "rep_reward": 750,
    },
]


def boss_race(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT reputation
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    reputation = player[0]

    available_bosses = [
        boss for boss in BOSSES
        if reputation >= boss["required_rep"]
    ]

    if not available_bosses:
        db.close()
        return """
🏆 Boss Race Locked

You need at least 100 reputation to challenge your first boss.
"""

    boss = available_bosses[-1]
    db.close()

    energy_ok, message = spend_energy(username, 2)

    if not energy_ok:
        return f"""
⚡ Boss Race Denied

{message}

Boss races cost 2 energy.
"""

    event = get_today_world_event()

    db = connect()
    cur = db.cursor()

    car = cur.execute("""
        SELECT horsepower, handling, grip, reliability, condition, oil, tires, engine_wear
        FROM cars
        WHERE owner = ? AND is_active = 1
    """, (username,)).fetchone()

    if not car:
        db.close()
        return "No active car found."

    horsepower, handling, grip, reliability, condition, oil, tires, engine_wear = car

    adjusted_grip = grip + event["grip_modifier"]

    player_score = (
        horsepower
        + handling
        + adjusted_grip
        + reliability
        + random.randint(-60, 60)
        - (100 - condition)
        - (100 - oil)
        - (100 - tires)
        - engine_wear
    )

    boss_score = boss["rating"] + random.randint(-40, 40)

    wear_bonus = event["wear_modifier"]

    tire_loss = random.randint(6, 12) + wear_bonus
    oil_loss = random.randint(5, 10) + wear_bonus
    engine_damage = random.randint(3, 8) + wear_bonus
    condition_loss = random.randint(5, 12) + wear_bonus

    cur.execute("""
        UPDATE cars
        SET tires = MAX(tires - ?, 0),
            oil = MAX(oil - ?, 0),
            engine_wear = engine_wear + ?,
            condition = MAX(condition - ?, 0)
        WHERE owner = ? AND is_active = 1
    """, (tire_loss, oil_loss, engine_damage, condition_loss, username))

    if player_score >= boss_score:
        event_bonus = int(boss["payout"] * (event["payout_modifier"] / 100))
        payout = boss["payout"] + event_bonus
        rep_reward = boss["rep_reward"] + event["rep_modifier"]

        cur.execute("""
            UPDATE players
            SET money = money + ?,
                reputation = reputation + ?
            WHERE username = ?
        """, (
            payout,
            rep_reward,
            username,
        ))

        result = f"""
🏆 Boss Race Victory

World Event:
{event['name']}

Boss:
{boss['name']} - {boss['title']}

Boss Car:
{boss['car']}

You beat the boss.

Base Money: ${boss['payout']}
World Event Bonus: +${event_bonus}
Total Money: ${payout}
Reputation: +{rep_reward}

Energy:
-2

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""

        result += unlock_achievement(username, "first_boss")

    else:
        rep_gain = random.randint(10, 25) + event["rep_modifier"]

        cur.execute("""
            UPDATE players
            SET reputation = reputation + ?
            WHERE username = ?
        """, (rep_gain, username))

        result = f"""
🏆 Boss Race Failed

World Event:
{event['name']}

Boss:
{boss['name']} - {boss['title']}

Boss Car:
{boss['car']}

You lost, but the streets noticed.

Reputation: +{rep_gain}

Energy:
-2

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""

    db.commit()
    db.close()

    result += check_progress_achievements(username)

    return result
