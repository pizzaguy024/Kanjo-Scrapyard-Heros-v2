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
    "Quit",
]


class KanjoWindow:
    def __init__(self):
        pygame.init()
        init_db()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Kanjo: Scrap Yard Heroes V2")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.small_font = pygame.font.SysFont("consolas", 19)
        self.title_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.logo_font = pygame.font.SysFont("consolas", 58, bold=True)

        self.username = ""
        self.input_text = ""
        self.mode = "title"

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

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_background(self):
        try:
            image = pygame.image.load(self.resource_path("assets/background.png")).convert()
            return pygame.transform.scale(image, (WIDTH, HEIGHT))
        except Exception:
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill((15, 15, 20))
            return surface

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

    def draw_panel(self):
        panel = pygame.Surface((1000, 610), pygame.SRCALPHA)
        panel.fill(BOX_BG)
        self.screen.blit(panel, (140, 70))
        pygame.draw.rect(self.screen, BOX_BORDER, (140, 70, 1000, 610), 2)

    def draw_input_box(self, label, y):
        input_box = pygame.Surface((880, 45), pygame.SRCALPHA)
        input_box.fill(INPUT_BG)
        self.screen.blit(input_box, (200, y))
        pygame.draw.rect(self.screen, RED, (200, y, 880, 45), 2)

        display_text = self.input_text
        if self.cursor_visible:
            display_text += "|"

        rendered = self.font.render(f"{label}: {display_text}", True, WHITE)
        self.screen.blit(rendered, (215, y + 9))

    def draw_wrapped_text(self, text, x, y, max_width, line_height, font, color=WHITE, max_y=610):
        lines = []

        for raw_line in text.split("\n"):
            if raw_line.strip() == "":
                lines.append("")
                continue

            words = raw_line.split(" ")
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

            lines.append(current_line)

        for line in lines:
            if y > max_y:
                more = font.render("...press ENTER to continue", True, RED)
                self.screen.blit(more, (x, y))
                break

            rendered = font.render(line, True, color)
            self.screen.blit(rendered, (x, y))
            y += line_height

    def draw_title_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        self.screen.blit(overlay, (0, 0))

        title_1 = self.logo_font.render("KANJO", True, RED)
        title_2 = self.title_font.render("SCRAP YARD HEROES", True, WHITE)

        self.screen.blit(title_1, (WIDTH // 2 - title_1.get_width() // 2, 230))
        self.screen.blit(title_2, (WIDTH // 2 - title_2.get_width() // 2, 300))

        if self.cursor_visible:
            start_text = self.font.render("PRESS ENTER TO START", True, WHITE)
            self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 430))

        tagline = self.small_font.render("Every legend starts as scrap.", True, RED)
        self.screen.blit(tagline, (WIDTH // 2 - tagline.get_width() // 2, 485))

    def draw_save_menu(self):
        self.draw_panel()

        title = self.title_font.render("DRIVER SELECT", True, RED)
        self.screen.blit(title, (200, 105))

        text = """
1. New Driver
2. Load Driver
3. View Drivers
4. Delete Driver
5. Credits
6. Quit

Choose an option.
"""
        self.draw_wrapped_text(text, 200, 180, 880, 32, self.font, max_y=520)
        self.draw_input_box("Choice", 585)

    def draw_new_driver_screen(self):
        self.draw_panel()

        title = self.title_font.render("NEW DRIVER", True, RED)
        self.screen.blit(title, (200, 105))

        intro = """
The gates are locked.
The yard is quiet.
Only the rain, rust, and old metal are keeping you company.

Enter a new driver name.
"""
        self.draw_wrapped_text(intro, 200, 175, 880, 30, self.font, max_y=520)
        self.draw_input_box("Driver Name", 585)

    def draw_load_driver_screen(self):
        self.draw_panel()

        title = self.title_font.render("LOAD DRIVER", True, RED)
        self.screen.blit(title, (200, 105))

        drivers = self.get_driver_list_text()

        text = f"""
Existing Drivers:

{drivers}

Type the exact driver name to load.
"""
        self.draw_wrapped_text(text, 200, 165, 880, 27, self.small_font, max_y=540)
        self.draw_input_box("Driver Name", 585)

    def draw_delete_driver_screen(self):
        self.draw_panel()

        title = self.title_font.render("DELETE DRIVER", True, RED)
        self.screen.blit(title, (200, 105))

        drivers = self.get_driver_list_text()

        text = f"""
Existing Drivers:

{drivers}

Type the exact driver name to DELETE.

Warning:
This permanently deletes the player, cars, and achievements.
"""
        self.draw_wrapped_text(text, 200, 155, 880, 25, self.small_font, max_y=540)
        self.draw_input_box("Delete Name", 585)

    def draw_story_screen(self):
        self.draw_panel()

        title = self.title_font.render("THE BEGINNING", True, RED)
        self.screen.blit(title, (200, 105))

        self.draw_wrapped_text(
            self.story_visible_text,
            200,
            170,
            880,
            30,
            self.font,
            max_y=575,
        )

        if self.story_index >= len(self.story_full_text):
            hint = self.small_font.render("Press ENTER to enter the garage.", True, RED)
            self.screen.blit(hint, (200, 630))
        else:
            hint = self.small_font.render("Typing story...", True, RED)
            self.screen.blit(hint, (200, 630))

    def draw_menu_screen(self):
        self.draw_panel()

        title = self.title_font.render("KANJO: SCRAP YARD HEROES V2", True, RED)
        self.screen.blit(title, (200, 95))

        left_x = 200
        right_x = 660
        start_y = 155
        line_gap = 25

        for index, option in enumerate(MENU_OPTIONS, start=1):
            if index <= 11:
                x = left_x
                y = start_y + ((index - 1) * line_gap)
            else:
                x = right_x
                y = start_y + ((index - 12) * line_gap)

            line = self.small_font.render(f"{index}. {option}", True, WHITE)
            self.screen.blit(line, (x, y))

        hint = self.small_font.render("Type a menu number, then press ENTER.", True, RED)
        self.screen.blit(hint, (200, 535))

        self.draw_input_box("Choice", 585)

    def draw_output_screen(self):
        self.draw_panel()

        title = self.title_font.render("KANJO REPORT", True, RED)
        self.screen.blit(title, (200, 95))

        self.draw_wrapped_text(
            self.output_text,
            200,
            150,
            880,
            24,
            self.small_font,
            max_y=600,
        )

        hint = self.small_font.render("Press ENTER to return. Press ESC for driver select.", True, RED)
        self.screen.blit(hint, (200, 635))

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
        self.mode = "story"

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
            self.mode = "buy_car"
            self.input_text = ""
            return "Enter dealer car number: 1, 2, or 3"
        if choice == "11":
            return view_owned_cars(self.username)
        if choice == "12":
            self.mode = "switch_car"
            self.input_text = ""
            return "Enter the car ID you want to drive."
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
            return MUSIC_CREDIT
        if choice == "21":
            self.mode = "save_menu"
            return "Returning to driver select."

        return "Invalid choice."

    def handle_enter(self):
        if self.mode == "title":
            self.mode = "save_menu"
            self.input_text = ""
            return

        if self.mode == "save_menu":
            choice = self.input_text.strip()
            self.input_text = ""

            if choice == "1":
                self.mode = "new_driver"
            elif choice == "2":
                self.mode = "load_driver"
            elif choice == "3":
                self.output_text = f"""
Saved Drivers:

{self.get_driver_list_text()}
"""
                self.mode = "output"
            elif choice == "4":
                self.mode = "delete_driver"
            elif choice == "5":
                self.output_text = MUSIC_CREDIT
                self.mode = "output"
            elif choice == "6":
                pygame.quit()
                sys.exit()
            else:
                self.output_text = "Invalid choice."
                self.mode = "output"
            return

        if self.mode == "new_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            if self.player_exists(name):
                self.output_text = "That driver already exists. Use Load Driver instead."
                self.mode = "output"
                return

            self.username = name
            create_player(self.username)
            starter_car = self.get_active_car_name(self.username)
            self.start_story(self.username, starter_car, is_new_player=True)
            return

        if self.mode == "load_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            if not self.player_exists(name):
                self.output_text = "No driver found with that name."
                self.mode = "output"
                return

            self.username = name
            starter_car = self.get_active_car_name(self.username)
            self.start_story(self.username, starter_car, is_new_player=False)
            return

        if self.mode == "delete_driver":
            name = self.input_text.strip()
            self.input_text = ""

            if not name:
                return

            self.output_text = self.delete_driver(name)
            self.mode = "output"
            return

        if self.mode == "story":
            if self.story_index < len(self.story_full_text):
                self.story_visible_text = self.story_full_text
                self.story_index = len(self.story_full_text)
            else:
                self.input_text = ""
                self.mode = "menu"
            return

        if self.mode == "menu":
            result = self.run_menu_choice(self.input_text.strip())

            if self.mode in ["buy_car", "switch_car", "save_menu"]:
                self.output_text = result
            else:
                self.output_text = result
                self.mode = "output"

            self.input_text = ""
            return

        if self.mode == "buy_car":
            self.output_text = buy_dealer_car(
                self.username,
                self.current_dealer_cars,
                self.input_text.strip(),
            )
            self.input_text = ""
            self.mode = "output"
            return

        if self.mode == "switch_car":
            self.output_text = switch_active_car(
                self.username,
                self.input_text.strip(),
            )
            self.input_text = ""
            self.mode = "output"
            return

        if self.mode == "output":
            self.input_text = ""
            if self.username:
                self.mode = "menu"
            else:
                self.mode = "save_menu"
            return

    def run(self):
        while True:
            self.clock.tick(60)
            self.update_cursor()
            self.update_story_typing()

            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_enter()

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    elif event.key == pygame.K_ESCAPE:
                        if self.mode in ["menu", "story", "output", "buy_car", "switch_car"]:
                            self.mode = "save_menu"
                            self.input_text = ""
                            self.username = ""

                        elif self.mode in ["new_driver", "load_driver", "delete_driver"]:
                            self.mode = "save_menu"
                            self.input_text = ""

                    else:
                        typing_modes = [
                            "save_menu",
                            "new_driver",
                            "load_driver",
                            "delete_driver",
                            "menu",
                            "buy_car",
                            "switch_car",
                        ]

                        if self.mode in typing_modes:
                            if len(self.input_text) < 40 and event.unicode:
                                self.input_text += event.unicode

            if self.mode == "title":
                self.draw_title_screen()
            elif self.mode == "save_menu":
                self.draw_save_menu()
            elif self.mode == "new_driver":
                self.draw_new_driver_screen()
            elif self.mode == "load_driver":
                self.draw_load_driver_screen()
            elif self.mode == "delete_driver":
                self.draw_delete_driver_screen()
            elif self.mode == "story":
                self.draw_story_screen()
            elif self.mode == "menu":
                self.draw_menu_screen()
            else:
                self.draw_output_screen()

            pygame.display.flip()
