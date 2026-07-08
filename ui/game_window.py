import pygame
import sys
import os

from database import init_db, connect
from systems.player_system import create_player, profile
from systems.garage_system import garage, repair_car, upgrade_car, upgrade_garage
from systems.race_system import race_ai
from systems.daily_system import claim_daily_reward
from systems.boss_system import boss_race
from systems.world_event_system import view_world_event
from systems.achievement_system import view_achievements
from systems.stats_system import view_stats
from systems.leaderboard_system import (
    reputation_leaderboard,
    money_leaderboard,
    garage_leaderboard,
    car_power_leaderboard,
)
from systems.dealer_system import (
    view_dealer,
    buy_dealer_car,
    view_owned_cars,
    switch_active_car,
)
from ui.audio import AudioManager
from ui.screens.title_screen import TitleScreen
from ui.screens.save_screen import SaveScreen
from ui.screens.text_input_screen import TextInputScreen
from ui.screens.story_screen import StoryScreen
from ui.screens.menu_screen import MenuScreen
from ui.screens.output_screen import OutputScreen


class KanjoWindow:
    WIDTH = 1280
    HEIGHT = 720

    WHITE = (235, 235, 235)
    RED = (220, 40, 50)
    BOX_BG = (0, 0, 0, 200)
    INPUT_BG = (15, 15, 20, 230)
    BOX_BORDER = (230, 230, 230)

    MUSIC_CREDIT = """
Music Credit

"12am"
by Paint The Skies

Music from #Uppbeat (free for Creators!)
https://uppbeat.io/t/paint-the-skies/12am
"""

    MENU_OPTIONS = [
        "Profile",
        "Garage",
        "Race AI",
        "Repair Car",
        "Upgrade Car",
        "Upgrade Garage",
        "Daily Login Reward",
        "Boss Race",
        "View Scrap Yard Dealer",
        "Buy Dealer Car",
        "View Owned Cars",
        "Switch Active Car",
        "View Daily World Event",
        "View Achievements",
        "View Stats",
        "Reputation Leaderboard",
        "Money Leaderboard",
        "Garage Leaderboard",
        "Car Power Leaderboard",
        "Credits",
        "Driver Select",
    ]

    def __init__(self):
        pygame.init()
        init_db()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Kanjo: Scrap Yard Heroes V2")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.small_font = pygame.font.SysFont("consolas", 19)
        self.title_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.logo_font = pygame.font.SysFont("consolas", 58, bold=True)

        self.username = ""
        self.input_text = ""
        self.mode = "title"
        self.previous_mode = "save"

        self.output_text = ""
        self.story_full_text = ""
        self.story_visible_text = ""
        self.story_index = 0
        self.story_timer = 0

        self.current_dealer_cars = []

        self.cursor_timer = 0
        self.cursor_visible = True

        self.background = self.load_background()

        try:
            icon = pygame.image.load(self.resource_path("assets/icon.png"))
            pygame.display.set_icon(icon)
        except Exception:
            pass

        self.audio = AudioManager(self.resource_path)
        self.audio.play_music("assets/audio/title_theme.mp3")
        self.audio.load_sound("click", "assets/audio/click.wav")
        self.audio.load_sound("hover", "assets/audio/hover.wav")

        self.screens = {
            "title": TitleScreen(self),
            "save": SaveScreen(self),
            "input": TextInputScreen(self),
            "story": StoryScreen(self),
            "menu": MenuScreen(self),
            "output": OutputScreen(self),
        }

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_background(self):
        try:
            image = pygame.image.load(self.resource_path("assets/background.png")).convert()
            return pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        except Exception:
            surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            surface.fill((15, 15, 20))
            return surface

    def draw_panel(self):
        panel = pygame.Surface((1000, 610), pygame.SRCALPHA)
        panel.fill(self.BOX_BG)
        self.screen.blit(panel, (140, 70))
        pygame.draw.rect(self.screen, self.BOX_BORDER, (140, 70, 1000, 610), 2)

    def update_cursor(self):
        self.cursor_timer += self.clock.get_time()
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def update_story_typing(self):
        if self.mode != "story":
            return

        self.story_timer += self.clock.get_time()

        if self.story_timer >= 22 and self.story_index < len(self.story_full_text):
            self.story_visible_text += self.story_full_text[self.story_index]
            self.story_index += 1
            self.story_timer = 0

    def set_mode(self, mode):
        self.mode = mode

    def show_output(self, text, previous_mode=None):
        self.output_text = text
        self.previous_mode = previous_mode or self.mode
        self.set_mode("output")

    def player_exists(self, username):
        db = connect()
        cur = db.cursor()
        player = cur.execute(
            "SELECT username FROM players WHERE username = ?",
            (username,),
        ).fetchone()
        db.close()
        return player is not None

    def get_driver_names(self):
        db = connect()
        cur = db.cursor()

        drivers = cur.execute("""
            SELECT username
            FROM players
            ORDER BY username COLLATE NOCASE
        """).fetchall()

        db.close()
        return [driver[0] for driver in drivers]

    def get_driver_list_text(self):
        drivers = self.get_driver_names()

        if not drivers:
            return "No drivers found."

        lines = []
        for index, driver in enumerate(drivers, start=1):
            lines.append(f"{index}. {driver}")

        return "\n".join(lines)

    def delete_driver(self, username):
        if not self.player_exists(username):
            return "No driver found with that name."

        db = connect()
        cur = db.cursor()

        cur.execute("DELETE FROM cars WHERE owner = ?", (username,))
        cur.execute("DELETE FROM achievements WHERE username = ?", (username,))
        cur.execute("DELETE FROM players WHERE username = ?", (username,))

        db.commit()
        db.close()

        return f"""
Driver Deleted

{username} has been removed from the scrapyard.
"""

    def get_active_car_name(self, username):
        db = connect()
        cur = db.cursor()
        car = cur.execute("""
            SELECT name
            FROM cars
            WHERE owner = ? AND is_active = 1
        """, (username,)).fetchone()
        db.close()

        if car:
            return car[0]

        return "a forgotten scrap yard machine"

    def start_story(self, username, starter_car, is_new_player=True):
        if username.strip().upper() == "BUSTER" and is_new_player:
            self.story_full_text = """
Neon light buzzed overhead.

BUSTER groaned, pushing himself off the damp alley asphalt. His head throbbed from a long night of underground clubbing after the races.

He stumbled toward the street, his fingers wrapping around his keys.

There she sat.

Wedged safely by a dumpster was his 1995 Mitsubishi Eclipse.

The lime-green paint practically glowed.

No scratches. No dents.

BUSTER smirked, sliding into the Sparco seat.

He turned the key.

The turbocharged engine roared to life, instantly clearing his head.

He shifted into first and rolled out into the Kanjo morning.
"""
        elif is_new_player:
            self.story_full_text = f"""
Late one night, {username} was working the final shift at the scrapyard.

The rain had turned the dirt paths into mud, and the rows of forgotten machines sat quietly under the broken security lights.

Near the back fence, half-buried beneath tarps, rust, and old parts, something caught your eye.

It was a {starter_car}.

Most people would have seen junk.

But you saw a beginning.

A few turns of the wrench. A little fuel. A spark.

The engine coughed, fought back, then came alive.

From that moment on, the scrapyard was no longer where your story ended.

It was where your legend began.
"""
        else:
            self.story_full_text = f"""
Welcome back, {username}.

Your car is waiting.

The streets remember your name, but legends are never finished.

Tonight, the journey continues.
"""

        self.story_visible_text = ""
        self.story_index = 0
        self.story_timer = 0
        self.set_mode("story")

    def configure_input_screen(self, title, body, label, action):
        self.screens["input"].configure(title, body, label, action)
        self.set_mode("input")

    def handle_title_action(self, action):
        if action == "start":
            self.set_mode("save")

    def handle_save_action(self, action):
        if action == "new_driver":
            self.configure_input_screen(
                "NEW DRIVER",
                """
The gates are locked.
The yard is quiet.
Only the rain, rust, and old metal are keeping you company.

Enter a new driver name.
""",
                "Driver Name",
                "confirm_new_driver",
            )
        elif action == "load_driver":
            self.configure_input_screen(
                "LOAD DRIVER",
                f"""
Existing Drivers:

{self.get_driver_list_text()}

Type the exact driver name to load.
""",
                "Driver Name",
                "confirm_load_driver",
            )
        elif action == "view_drivers":
            self.show_output(f"""
Saved Drivers:

{self.get_driver_list_text()}
""", previous_mode="save")
        elif action == "delete_driver":
            self.configure_input_screen(
                "DELETE DRIVER",
                f"""
Existing Drivers:

{self.get_driver_list_text()}

Type the exact driver name to DELETE.

Warning:
This permanently deletes the player, cars, and achievements.
""",
                "Delete Name",
                "confirm_delete_driver",
            )
        elif action == "credits":
            self.show_output(self.MUSIC_CREDIT, previous_mode="save")
        elif action == "quit":
            pygame.quit()
            sys.exit()

    def handle_input_action(self, action):
        if action == "back_to_save":
            self.input_text = ""
            self.set_mode("save")
            return

        if action == "confirm_new_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            if self.player_exists(name):
                self.show_output("That driver already exists. Use Load Driver instead.", previous_mode="save")
                return

            self.username = name
            create_player(self.username)
            starter_car = self.get_active_car_name(self.username)
            self.start_story(self.username, starter_car, is_new_player=True)

        elif action == "confirm_load_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            if not self.player_exists(name):
                self.show_output("No driver found with that name.", previous_mode="save")
                return

            self.username = name
            starter_car = self.get_active_car_name(self.username)
            self.start_story(self.username, starter_car, is_new_player=False)

        elif action == "confirm_delete_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            self.show_output(self.delete_driver(name), previous_mode="save")

    def handle_story_action(self, action):
        if action == "back_to_save":
            self.username = ""
            self.set_mode("save")
            return

        if action == "skip_story":
            self.story_visible_text = self.story_full_text
            self.story_index = len(self.story_full_text)
            self.set_mode("menu")
            return

        if action == "continue_story":
            if self.story_index < len(self.story_full_text):
                self.story_visible_text = self.story_full_text
                self.story_index = len(self.story_full_text)
            else:
                self.set_mode("menu")

    def run_menu_choice(self, choice):
        if choice == "1":
            return profile(self.username)
        if choice == "2":
            return garage(self.username)
        if choice == "3":
            return race_ai(self.username)
        if choice == "4":
            return repair_car(self.username)
        if choice == "5":
            return upgrade_car(self.username)
        if choice == "6":
            return upgrade_garage(self.username)
        if choice == "7":
            return claim_daily_reward(self.username)
        if choice == "8":
            return boss_race(self.username)
        if choice == "9":
            dealer_text, self.current_dealer_cars = view_dealer()
            return dealer_text
        if choice == "10":
            if not self.current_dealer_cars:
                return "View the Scrap Yard Dealer first."
            self.configure_input_screen(
                "BUY DEALER CAR",
                "Enter dealer car number: 1, 2, or 3",
                "Car Number",
                "confirm_buy_car",
            )
            return None
        if choice == "11":
            return view_owned_cars(self.username)
        if choice == "12":
            self.configure_input_screen(
                "SWITCH ACTIVE CAR",
                "Enter the car ID you want to drive.",
                "Car ID",
                "confirm_switch_car",
            )
            return None
        if choice == "13":
            return view_world_event()
        if choice == "14":
            return view_achievements(self.username)
        if choice == "15":
            return view_stats(self.username)
        if choice == "16":
            return reputation_leaderboard()
        if choice == "17":
            return money_leaderboard()
        if choice == "18":
            return garage_leaderboard()
        if choice == "19":
            return car_power_leaderboard()
        if choice == "20":
            return self.MUSIC_CREDIT
        if choice == "21":
            self.username = ""
            self.set_mode("save")
            return None

        return "Invalid choice."

    def handle_menu_action(self, action):
        result = self.run_menu_choice(action)

        if result is not None:
            self.show_output(result, previous_mode="menu")

    def handle_output_action(self, action):
        if action == "back_to_save":
            self.username = ""
            self.set_mode("save")
            return

        if self.username:
            self.set_mode("menu")
        else:
            self.set_mode("save")

    def handle_special_input_actions(self, action):
        if action == "confirm_buy_car":
            self.show_output(
                buy_dealer_car(self.username, self.current_dealer_cars, self.input_text.strip()),
                previous_mode="menu",
            )
            self.input_text = ""
            return True

        if action == "confirm_switch_car":
            self.show_output(
                switch_active_car(self.username, self.input_text.strip()),
                previous_mode="menu",
            )
            self.input_text = ""
            return True

        return False

    def handle_action(self, action):
        if not action:
            return

        self.audio.play_sound("click")

        if action in ["confirm_buy_car", "confirm_switch_car"]:
            if self.handle_special_input_actions(action):
                return

        if self.mode == "title":
            self.handle_title_action(action)
        elif self.mode == "save":
            self.handle_save_action(action)
        elif self.mode == "input":
            self.handle_input_action(action)
        elif self.mode == "story":
            self.handle_story_action(action)
        elif self.mode == "menu":
            self.handle_menu_action(action)
        elif self.mode == "output":
            self.handle_output_action(action)

    def current_screen(self):
        return self.screens.get(self.mode, self.screens["title"])

    def run(self):
        while True:
            self.clock.tick(60)
            self.update_cursor()
            self.update_story_typing()

            self.screen.blit(self.background, (0, 0))

            screen = self.current_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                action = screen.handle_event(event)
                self.handle_action(action)

            self.current_screen().draw()

            pygame.display.flip()
