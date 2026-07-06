import random
from datetime import date
from database import connect


WORLD_EVENTS = [
    {
        "name": "Clear Streets",
        "description": "The streets are calm tonight. No special modifiers.",
        "grip_modifier": 0,
        "payout_modifier": 0,
        "rep_modifier": 0,
        "wear_modifier": 0,
    },
    {
        "name": "Heavy Rain",
        "description": "Rain slicks the expressway. Grip is down, but reputation gains are higher.",
        "grip_modifier": -20,
        "payout_modifier": 0,
        "rep_modifier": 5,
        "wear_modifier": 2,
    },
    {
        "name": "Police Crackdown",
        "description": "Police are everywhere. Illegal races pay more, but wear and risk increase.",
        "grip_modifier": 0,
        "payout_modifier": 25,
        "rep_modifier": 10,
        "wear_modifier": 4,
    },
    {
        "name": "Street Festival",
        "description": "Crowds are out tonight. Everyone wants to see wild builds.",
        "grip_modifier": 0,
        "payout_modifier": 10,
        "rep_modifier": 15,
        "wear_modifier": 0,
    },
    {
        "name": "Heat Wave",
        "description": "Engines run hot. More engine wear from racing.",
        "grip_modifier": 0,
        "payout_modifier": 0,
        "rep_modifier": 0,
        "wear_modifier": 5,
    },
    {
        "name": "Dense Fog",
        "description": "Visibility is terrible. Handling matters more than horsepower tonight.",
        "grip_modifier": -10,
        "payout_modifier": 5,
        "rep_modifier": 5,
        "wear_modifier": 1,
    },
]


def init_world_event_table():
    db = connect()
    cur = db.cursor()

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


def get_today_world_event():
    init_world_event_table()

    today = date.today().isoformat()

    db = connect()
    cur = db.cursor()

    existing = cur.execute("""
        SELECT name, description, grip_modifier, payout_modifier, rep_modifier, wear_modifier
        FROM world_events
        WHERE event_date = ?
    """, (today,)).fetchone()

    if existing:
        db.close()
        return {
            "name": existing[0],
            "description": existing[1],
            "grip_modifier": existing[2],
            "payout_modifier": existing[3],
            "rep_modifier": existing[4],
            "wear_modifier": existing[5],
        }

    event = random.choice(WORLD_EVENTS)

    cur.execute("""
        INSERT INTO world_events (
            event_date, name, description,
            grip_modifier, payout_modifier, rep_modifier, wear_modifier
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        today,
        event["name"],
        event["description"],
        event["grip_modifier"],
        event["payout_modifier"],
        event["rep_modifier"],
        event["wear_modifier"],
    ))

    db.commit()
    db.close()

    return event


def view_world_event():
    event = get_today_world_event()

    return f"""
🌎 Daily World Event

{event['name']}

{event['description']}

Modifiers:
Grip: {event['grip_modifier']}
Payout: {event['payout_modifier']}%
Reputation: +{event['rep_modifier']}
Wear: +{event['wear_modifier']}
"""
