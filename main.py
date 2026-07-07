from ui.game_window import KanjoWindow
import traceback


def main():
    try:
        game = KanjoWindow()
        game.run()
    except Exception:
        print("\nGAME CRASHED:")
        print(traceback.format_exc())
        input("\nPress ENTER to close...")


if __name__ == "__main__":
    main()
