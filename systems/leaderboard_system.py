from database import connect


def reputation_leaderboard(limit=10):
    db = connect()
    cur = db.cursor()

    players = cur.execute("""
        SELECT username, reputation, money, garage_level
        FROM players
        ORDER BY reputation DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    if not players:
        return "No players found."

    text = "\n🏆 Reputation Leaderboard\n"

    for index, player in enumerate(players, start=1):
        username, reputation, money, garage_level = player
        text += f"""
#{index} {username}
Reputation: {reputation}
Money: ${money}
Garage Level: {garage_level}
"""

    return text


def money_leaderboard(limit=10):
    db = connect()
    cur = db.cursor()

    players = cur.execute("""
        SELECT username, money, reputation, garage_level
        FROM players
        ORDER BY money DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    if not players:
        return "No players found."

    text = "\n💰 Money Leaderboard\n"

    for index, player in enumerate(players, start=1):
        username, money, reputation, garage_level = player
        text += f"""
#{index} {username}
Money: ${money}
Reputation: {reputation}
Garage Level: {garage_level}
"""

    return text


def garage_leaderboard(limit=10):
    db = connect()
    cur = db.cursor()

    players = cur.execute("""
        SELECT username, garage_level, reputation, money
        FROM players
        ORDER BY garage_level DESC, reputation DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    if not players:
        return "No players found."

    text = "\n🏚️ Garage Leaderboard\n"

    for index, player in enumerate(players, start=1):
        username, garage_level, reputation, money = player
        text += f"""
#{index} {username}
Garage Level: {garage_level}
Reputation: {reputation}
Money: ${money}
"""

    return text


def car_power_leaderboard(limit=10):
    db = connect()
    cur = db.cursor()

    cars = cur.execute("""
        SELECT owner, name, horsepower, handling, grip, reliability,
               condition, upgrade_level
        FROM cars
        ORDER BY (horsepower + handling + grip + reliability) DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    if not cars:
        return "No cars found."

    text = "\n🚗 Car Power Leaderboard\n"

    for index, car in enumerate(cars, start=1):
        owner, name, horsepower, handling, grip, reliability, condition, upgrade_level = car
        power_score = horsepower + handling + grip + reliability

        text += f"""
#{index} {owner}
Car: {name}
Power Score: {power_score}
HP: {horsepower}
Handling: {handling}
Grip: {grip}
Reliability: {reliability}
Condition: {condition}%
Upgrade Level: {upgrade_level}
"""

    return text


def leaderboard_menu():
    return """
🏆 Leaderboards

1. Reputation Leaderboard
2. Money Leaderboard
3. Garage Leaderboard
4. Car Power Leaderboard
"""
