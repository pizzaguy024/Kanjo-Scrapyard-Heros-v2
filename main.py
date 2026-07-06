from database import init_db
from systems.player_system import create_player, profile
from systems.garage_system import garage, repair_car, upgrade_car, upgrade_garage
from systems.race_system import race_ai


def menu():
    print("\n=== KANJO: SCRAP YARD HEROES V2 ===")
    print("1. Start New Player")
    print("2. Profile")
    print("3. Garage")
    print("4. Race AI")
    print("5. Repair Car")
    print("6. Upgrade Car")
    print("7. Upgrade Garage")
    print("8. Quit")


def main():
    init_db()

    username = input("Enter your player name: ").strip()

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
            print("Later, street runner.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
