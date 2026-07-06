from datetime import date
from database import connect


def reset_energy_if_needed(username):
    today = date.today().isoformat()

    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT max_energy, last_energy_reset
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return

    max_energy, last_reset = player

    if last_reset != today:
        cur.execute("""
            UPDATE players
            SET energy = ?, last_energy_reset = ?
            WHERE username = ?
        """, (max_energy, today, username))

        db.commit()

    db.close()


def spend_energy(username, amount):
    reset_energy_if_needed(username)

    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT energy
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return False, "No player found."

    energy = player[0]

    if energy < amount:
        db.close()
        return False, "Not enough energy."

    cur.execute("""
        UPDATE players
        SET energy = energy - ?
        WHERE username = ?
    """, (amount, username))

    db.commit()
    db.close()

    return True, "Energy spent."
