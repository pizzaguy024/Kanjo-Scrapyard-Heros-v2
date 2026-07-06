from datetime import date, datetime, timedelta
from database import connect


DAILY_REWARDS = {
    1: {"money": 250, "energy": 0, "text": "$250"},
    2: {"money": 500, "energy": 0, "text": "$500"},
    3: {"money": 0, "energy": 2, "text": "+2 Energy"},
    4: {"money": 750, "energy": 0, "text": "$750"},
    5: {"money": 0, "repair": True, "text": "Free Repair"},
    6: {"money": 1000, "energy": 0, "text": "$1,000"},
    7: {"money": 2000, "energy": 3, "text": "$2,000 +3 Energy"},
}


def claim_daily_reward(username):
    today = date.today()
    today_text = today.isoformat()

    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT last_daily_reward, login_streak, max_energy
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    last_daily_reward, login_streak, max_energy = player

    if last_daily_reward == today_text:
        db.close()
        return """
📅 Daily Reward Already Claimed

You already claimed your daily reward today.
Come back tomorrow.
"""

    if last_daily_reward:
        last_date = datetime.strptime(last_daily_reward, "%Y-%m-%d").date()
        yesterday = today - timedelta(days=1)

        if last_date == yesterday:
            login_streak += 1
        else:
            login_streak = 1
    else:
        login_streak = 1

    reward_day = ((login_streak - 1) % 7) + 1
    reward = DAILY_REWARDS[reward_day]

    money_reward = reward.get("money", 0)
    energy_reward = reward.get("energy", 0)

    cur.execute("""
        UPDATE players
        SET money = money + ?,
            energy = MIN(energy + ?, max_energy),
            last_daily_reward = ?,
            login_streak = ?
        WHERE username = ?
    """, (
        money_reward,
        energy_reward,
        today_text,
        login_streak,
        username,
    ))

    if reward.get("repair"):
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
🎁 Daily Login Reward Claimed

Streak Day: {login_streak}
Reward Cycle Day: {reward_day}

Reward:
{reward['text']}
"""
