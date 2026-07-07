from database import connect


ACHIEVEMENTS = [
    {
        "key": "first_steps",
        "name": "First Steps",
        "description": "Create your first driver profile.",
    },
    {
        "key": "first_race",
        "name": "First Race",
        "description": "Complete your first AI race.",
    },
    {
        "key": "first_boss",
        "name": "Boss Hunter",
        "description": "Win your first boss race.",
    },
    {
        "key": "garage_lvl_2",
        "name": "Two-Car Setup",
        "description": "Upgrade your garage to Level 2.",
    },
    {
        "key": "garage_lvl_5",
        "name": "Scrap Yard Empire",
        "description": "Upgrade your garage to Level 5.",
    },
    {
        "key": "rep_500",
        "name": "Backroad Menace",
        "description": "Reach 500 reputation.",
    },
    {
        "key": "rep_5000",
        "name": "Midnight Threat",
        "description": "Reach 5,000 reputation.",
    },
    {
        "key": "rep_50000",
        "name": "Expressway King",
        "description": "Reach 50,000 reputation.",
    },
    {
        "key": "car_collector",
        "name": "Car Collector",
        "description": "Own 3 cars.",
    },
]


def init_achievement_table():
    db = connect()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            achievement_key TEXT NOT NULL,
            unlocked_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, achievement_key)
        )
    """)

    db.commit()
    db.close()


def unlock_achievement(username, achievement_key):
    init_achievement_table()

    achievement = next(
        (item for item in ACHIEVEMENTS if item["key"] == achievement_key),
        None
    )

    if not achievement:
        return ""

    db = connect()
    cur = db.cursor()

    already_unlocked = cur.execute("""
        SELECT achievement_key
        FROM achievements
        WHERE username = ? AND achievement_key = ?
    """, (username, achievement_key)).fetchone()

    if already_unlocked:
        db.close()
        return ""

    cur.execute("""
        INSERT INTO achievements (username, achievement_key)
        VALUES (?, ?)
    """, (username, achievement_key))

    db.commit()
    db.close()

    return f"""

🏅 Achievement Unlocked:
{achievement['name']}
{achievement['description']}
"""


def check_progress_achievements(username):
    init_achievement_table()

    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT reputation, garage_level
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    car_count = cur.execute("""
        SELECT COUNT(*)
        FROM cars
        WHERE owner = ?
    """, (username,)).fetchone()[0]

    db.close()

    if not player:
        return ""

    reputation, garage_level = player
    messages = ""

    if reputation >= 500:
        messages += unlock_achievement(username, "rep_500")

    if reputation >= 5000:
        messages += unlock_achievement(username, "rep_5000")

    if reputation >= 50000:
        messages += unlock_achievement(username, "rep_50000")

    if garage_level >= 2:
        messages += unlock_achievement(username, "garage_lvl_2")

    if garage_level >= 5:
        messages += unlock_achievement(username, "garage_lvl_5")

    if car_count >= 3:
        messages += unlock_achievement(username, "car_collector")

    return messages


def view_achievements(username):
    init_achievement_table()

    db = connect()
    cur = db.cursor()

    unlocked = cur.execute("""
        SELECT achievement_key
        FROM achievements
        WHERE username = ?
    """, (username,)).fetchall()

    db.close()

    unlocked_keys = [row[0] for row in unlocked]

    text = "\n🏅 Achievements\n"

    for achievement in ACHIEVEMENTS:
        status = "Unlocked" if achievement["key"] in unlocked_keys else "Locked"

        text += f"""
{achievement['name']}
Status: {status}
{achievement['description']}
"""

    return text
