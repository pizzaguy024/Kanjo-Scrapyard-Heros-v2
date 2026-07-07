from database import connect


def view_stats(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT races_entered, races_won, races_lost,
               boss_races_entered, boss_races_won, boss_races_lost,
               total_earnings, total_rep_earned
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
        return "No player found."

    races_entered, races_won, races_lost, boss_entered, boss_won, boss_lost, total_earnings, total_rep = player

    win_rate = 0
    if races_entered > 0:
        win_rate = round((races_won / races_entered) * 100, 1)

    boss_win_rate = 0
    if boss_entered > 0:
        boss_win_rate = round((boss_won / boss_entered) * 100, 1)

    return f"""
📊 Driver Stats

AI Races:
Entered: {races_entered}
Wins: {races_won}
Losses: {races_lost}
Win Rate: {win_rate}%

Boss Races:
Entered: {boss_entered}
Wins: {boss_won}
Losses: {boss_lost}
Boss Win Rate: {boss_win_rate}%

Career:
Total Earnings: ${total_earnings}
Total Reputation Earned: {total_rep}
Cars Owned: {car_count}
"""
