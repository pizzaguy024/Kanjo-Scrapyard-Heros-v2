from database import connect


GARAGE_LEVELS = {
    1: {"cost": 0, "max_energy": 10, "car_slots": 1, "repair_discount": 0},
    2: {"cost": 2500, "max_energy": 12, "car_slots": 2, "repair_discount": 5},
    3: {"cost": 6000, "max_energy": 14, "car_slots": 3, "repair_discount": 10},
    4: {"cost": 12000, "max_energy": 16, "car_slots": 4, "repair_discount": 15},
    5: {"cost": 25000, "max_energy": 18, "car_slots": 5, "repair_discount": 20},
}


def garage(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT garage_level, max_energy
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    car = cur.execute("""
        SELECT name, rarity, horsepower, handling, grip, reliability,
               condition, oil, tires, engine_wear, upgrade_level
        FROM cars
        WHERE owner = ? AND is_active = 1
    """, (username,)).fetchone()

    if not player or not car:
        db.close()
        return "No garage found."

    garage_level, max_energy = player
    db.close()

    next_level = garage_level + 1

    if next_level in GARAGE_LEVELS:
        next_data = GARAGE_LEVELS[next_level]
        next_text = f"""
Next Upgrade:
Garage Level {next_level}
Cost: ${next_data['cost']}
Max Energy: {next_data['max_energy']}
Car Slots: {next_data['car_slots']}
Repair Discount: {next_data['repair_discount']}%
"""
    else:
        next_text = "Garage fully upgraded."

    return f"""
🔧 Garage

Garage Level: {garage_level}
Max Energy: {max_energy}

Active Car:
{car[0]}
Rarity: {car[1]}

Stats:
Horsepower: {car[2]}
Handling: {car[3]}
Grip: {car[4]}
Reliability: {car[5]}

Condition:
Body: {car[6]}%
Oil: {car[7]}%
Tires: {car[8]}%
Engine Wear: {car[9]}%

Upgrade Level: {car[10]}

{next_text}
"""


def repair_car(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money, garage_level
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    money, garage_level = player
    repair_discount = GARAGE_LEVELS[garage_level]["repair_discount"]

    base_cost = 500
    discount = int(base_cost * (repair_discount / 100))
    final_cost = base_cost - discount

    if money < final_cost:
        db.close()
        return f"You need ${final_cost} to repair your car."

    cur.execute("""
        UPDATE players
        SET money = money - ?
        WHERE username = ?
    """, (final_cost, username))

    cur.execute("""
        UPDATE cars
        SET condition = 100,
            oil = 100,
            tires = 100,
            engine_wear = 0
        WHERE owner = ? AND is_active = 1
    """, (username,))

    db.commit()
    db.close()

    return f"""
🔧 Car repaired.

Base Cost: ${base_cost}
Garage Discount: {repair_discount}%
Final Cost: ${final_cost}
"""


def upgrade_car(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    car = cur.execute("""
        SELECT upgrade_level
        FROM cars
        WHERE owner = ? AND is_active = 1
    """, (username,)).fetchone()

    if not player or not car:
        db.close()
        return "No car found."

    money = player[0]
    upgrade_level = car[0]
    cost = 750 + upgrade_level * 500

    if money < cost:
        db.close()
        return f"You need ${cost} for the next car upgrade."

    cur.execute("""
        UPDATE players
        SET money = money - ?
        WHERE username = ?
    """, (cost, username))

    cur.execute("""
        UPDATE cars
        SET horsepower = horsepower + 15,
            handling = handling + 3,
            grip = grip + 3,
            reliability = reliability + 2,
            upgrade_level = upgrade_level + 1
        WHERE owner = ? AND is_active = 1
    """, (username,))

    db.commit()
    db.close()

    return f"⚙️ Car upgraded. Cost: ${cost}"


def upgrade_garage(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money, garage_level
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    money, garage_level = player
    next_level = garage_level + 1

    if next_level not in GARAGE_LEVELS:
        db.close()
        return "Garage is already max level."

    upgrade = GARAGE_LEVELS[next_level]
    cost = upgrade["cost"]

    if money < cost:
        db.close()
        return f"You need ${cost} to upgrade your garage."

    cur.execute("""
        UPDATE players
        SET money = money - ?,
            garage_level = ?,
            max_energy = ?,
            energy = ?
        WHERE username = ?
    """, (
        cost,
        next_level,
        upgrade["max_energy"],
        upgrade["max_energy"],
        username,
    ))

    db.commit()
    db.close()

    return f"""
🏚️ Garage upgraded to Level {next_level}.

Cost: ${cost}
Max Energy: {upgrade['max_energy']}
Car Slots: {upgrade['car_slots']}
Repair Discount: {upgrade['repair_discount']}%
"""
