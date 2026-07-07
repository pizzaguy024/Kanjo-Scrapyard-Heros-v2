from database import init_db
from systems.player_system import create_player, profile
from systems.garage_system import garage, repair_car, upgrade_car, upgrade_garage
from systems.race_system import race_ai
from systems.daily_system import claim_daily_reward
from systems.boss_system import boss_race
from systems.world_event_system import view_world_event
from systems.rank_system import format_rank_progress
from database import connect
from systems.dealer_system import (
    view_dealer,
    buy_dealer_car,
    view_owned_cars,
    switch_active_car,
)


def menu():
    print("\n=== KANJO: SCRAP YARD HEROES V2 ===")
    print("1. Start New Player")
    print("2. Profile")
    print("3. Garage")
    print("4. Race AI")
    print("5. Repair Car")
    print("6. Upgrade Car")
    print("7. Upgrade Garage")
    print("8. Daily Login Reward")
    print("9. Boss Race")
    print("10. View Scrap Yard Dealer")
    print("11. Buy Dealer Car")
    print("12. View Owned Cars")
    print("13. Switch Active Car")
    print("14. View Daily World Event")
    print("15. View Rank")
    print("16. Quit")


def view_rank(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT reputation
        FROM players
        WHERE username = ?
    """, (username,)).fetchone()

    db.close()

    if not player:
        return "No player found."

    return format_rank_progress(player[0])


def main():
    init_db()

    username = input("Enter your player name: ").strip()
    current_dealer_cars = []

    while True:
        menu()
        choice = input("> ").strip()

        if choice == "1":
            print(create_player(username))

        elif choice == "2":
            print(profile(username))

        elif choice == "3":
            print(garage(username))

        elif choice == "4":
            print(race_ai(username))

        elif choice == "5":
            print(repair_car(username))

        elif choice == "6":
            print(upgrade_car(username))

        elif choice == "7":
            print(upgrade_garage(username))

        elif choice == "8":
            print(claim_daily_reward(username))

        elif choice == "9":
            print(boss_race(username))

        elif choice == "10":
            dealer_text, current_dealer_cars = view_dealer()
            print(dealer_text)

        elif choice == "11":
            if not current_dealer_cars:
                print("View the Scrap Yard Dealer first.")
            else:
                car_choice = input("Which dealer car do you want to buy? 1, 2, or 3: ").strip()
                print(buy_dealer_car(username, current_dealer_cars, car_choice))

        elif choice == "12":
            print(view_owned_cars(username))

        elif choice == "13":
            car_id = input("Enter the car ID you want to drive: ").strip()
            print(switch_active_car(username, car_id))

        elif choice == "14":
            print(view_world_event())

        elif choice == "15":
            print(view_rank(username))

        elif choice == "16":
            print("Later, street runner.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
