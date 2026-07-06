import random
from database import connect


DEALER_CARS = [
    {"name": "1989 Honda CRX Si", "rarity": "Common", "price": 2500, "horsepower": 108, "handling": 78, "grip": 65, "reliability": 82},
    {"name": "1994 Honda Civic EG", "rarity": "Common", "price": 3000, "horsepower": 125, "handling": 72, "grip": 65, "reliability": 80},
    {"name": "1995 Mitsubishi Eclipse GS", "rarity": "Common", "price": 3500, "horsepower": 140, "handling": 68, "grip": 63, "reliability": 70},
    {"name": "1991 Nissan 240SX", "rarity": "Common", "price": 4500, "horsepower": 155, "handling": 72, "grip": 62, "reliability": 70},

    {"name": "1986 Toyota AE86", "rarity": "Rare", "price": 9000, "horsepower": 128, "handling": 85, "grip": 70, "reliability": 82},
    {"name": "1991 Mazda RX-7 FC", "rarity": "Rare", "price": 11000, "horsepower": 200, "handling": 82, "grip": 72, "reliability": 62},
    {"name": "1993 Nissan Silvia S13", "rarity": "Rare", "price": 12500, "horsepower": 205, "handling": 80, "grip": 70, "reliability": 68},

    {"name": "1997 Honda Civic Type R EK9", "rarity": "Very Rare", "price": 22000, "horsepower": 182, "handling": 88, "grip": 78, "reliability": 85},
    {"name": "1998 Acura Integra Type R DC2", "rarity": "Very Rare", "price": 24000, "horsepower": 195, "handling": 90, "grip": 80, "reliability": 84},
    {"name": "1993 Mazda RX-7 FD", "rarity": "Very Rare", "price": 35000, "horsepower": 255, "handling": 92, "grip": 82, "reliability": 58},
]


def get_player_car_limit(garage_level):
    return garage_level


def view_dealer():
    cars = random.sample(DEALER_CARS, 3)

    text = "\n🏚️ Scrap Yard Dealer\n\nToday's Finds:\n"

    for index, car in enumerate(cars, start=1):
        text += f"""
{index}. {car['name']}
Rarity: {car['rarity']}
Price: ${car['price']}
HP: {car['horsepower']}
Handling: {car['handling']}
Grip: {car['grip']}
Reliability: {car['reliability']}
"""

    text += """
To buy one, choose Buy Dealer Car from the menu and enter 1, 2, or 3.
Note: dealer inventory rerolls every time you view it in this test version.
"""

    return text, cars


def buy_dealer_car(username, dealer_cars, choice):
    try:
        choice = int(choice)
    except ValueError:
        return "Invalid choice."

    if choice < 1 or choice > len(dealer_cars):
        return "Invalid car number."

    selected_car = dealer_cars[choice - 1]

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
    car_limit = get_player_car_limit(garage_level)

    owned_count = cur.execute("""
        SELECT COUNT(*)
        FROM cars
        WHERE owner = ?
    """, (username,)).fetchone()[0]

    if owned_count >= car_limit:
        db.close()
        return f"""
🚫 Garage Full

You own {owned_count}/{car_limit} cars.
Upgrade your garage to buy more cars.
"""

    if money < selected_car["price"]:
        db.close()
        return f"""
Not enough money.

Car Price: ${selected_car['price']}
Your Money: ${money}
"""

    cur.execute("""
        UPDATE players
        SET money = money - ?
        WHERE username = ?
    """, (selected_car["price"], username))

    cur.execute("""
        INSERT INTO cars (
            owner, name, rarity, horsepower, handling, grip, reliability,
            condition, oil, tires, engine_wear, upgrade_level, is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        selected_car["name"],
        selected_car["rarity"],
        selected_car["horsepower"],
        selected_car["handling"],
        selected_car["grip"],
        selected_car["reliability"],
        80,
        100,
        100,
        0,
        0,
        0,
    ))

    db.commit()
    db.close()

    return f"""
✅ Car Purchased

{selected_car['name']}
Rarity: {selected_car['rarity']}
Price: ${selected_car['price']}

It has been added to your garage.
"""


def view_owned_cars(username):
    db = connect()
    cur = db.cursor()

    cars = cur.execute("""
        SELECT id, name, rarity, horsepower, handling, grip, reliability, condition, is_active
        FROM cars
        WHERE owner = ?
        ORDER BY id
    """, (username,)).fetchall()

    if not cars:
        db.close()
        return "You do not own any cars."

    db.close()

    text = "\n🚗 Owned Cars\n"

    for car in cars:
        active = "ACTIVE" if car[8] == 1 else "Stored"

        text += f"""
ID: {car[0]}
{car[1]}
Status: {active}
Rarity: {car[2]}
HP: {car[3]}
Handling: {car[4]}
Grip: {car[5]}
Reliability: {car[6]}
Condition: {car[7]}%
"""

    text += "\nUse Switch Active Car and enter the car ID."

    return text


def switch_active_car(username, car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return "Invalid car ID."

    db = connect()
    cur = db.cursor()

    car = cur.execute("""
        SELECT id, name
        FROM cars
        WHERE owner = ? AND id = ?
    """, (username, car_id)).fetchone()

    if not car:
        db.close()
        return "That car does not exist in your garage."

    cur.execute("""
        UPDATE cars
        SET is_active = 0
        WHERE owner = ?
    """, (username,))

    cur.execute("""
        UPDATE cars
        SET is_active = 1
        WHERE owner = ? AND id = ?
    """, (username, car_id))

    db.commit()
    db.close()

    return f"""
🔑 Active Car Switched

You are now driving:
{car[1]}
"""
