import pygame
import sys

from database import init_db
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


WIDTH = 1280
HEIGHT = 720

WHITE = (235, 235, 235)
RED = (220, 40, 50)
BLACK = (0, 0, 0)
BOX_BG = (0, 0, 0, 190)
BOX_BORDER = (230, 230, 230)

MENU_OPTIONS = [
    "Start New Player",
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
        self.small_font = pygame.font.SysFont("consolas", 20)
        self.title_font = pygame.font.SysFont("consolas", 34, bold=True)

        self.username = ""
        self.input_text = ""
        self.mode = "username"

        self.output_text = "Enter your player name to begin."
        self.current_dealer_cars = []

        self.background = self.load_background()

    def load_background(self):
        try:
            image = pygame.image.load("assets/background.png").convert()
            return pygame.transform.scale(image, (WIDTH, HEIGHT))
        except Exception:
            surface = pygame.Surface((WIDTH, HEIGHT))
            surface.fill((15, 15, 20))
            return surface

    def draw_text_box(self):
        box = pygame.Surface((960, 590), pygame.SRCALPHA)
        box.fill(BOX_BG)

        self.screen.blit(box, (160, 90))
        pygame.draw.rect(self.screen, BOX_BORDER, (160, 90, 960, 590), 2)

    def draw_wrapped_text(self, text, x, y, max_width, line_height, font, color=WHITE):
        lines = []

        for raw_line in text.split("\n"):
            words = raw_line.split(" ")

            if not words:
                lines.append("")
                continue

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
            rendered = font.render(line, True, color)
            self.screen.blit(rendered, (x, y))
            y += line_height

            if y > 640:
                break

    def draw_username_screen(self):
        self.draw_text_box()

        title = self.title_font.render("KANJO: SCRAP YARD HEROES V2", True, RED)
        self.screen.blit(title, (210, 125))

        self.draw_wrapped_text(
            self.output_text,
            210,
            190,
            850,
            28,
            self.font,
        )

        prompt = self.font.render(f"Player Name: {self.input_text}", True, WHITE)
        self.screen.blit(prompt, (210, 600))

    def draw_menu_screen(self):
        self.draw_text_box()

        title = self.title_font.render("KANJO: SCRAP YARD HEROES V2", True, RED)
        self.screen.blit(title, (210, 115))

        y = 165
        for index, option in enumerate(MENU_OPTIONS, start=1):
            line = self.small_font.render(f"{index}. {option}", True, WHITE)
            self.screen.blit(line, (210, y))
            y += 24

        pygame.draw.line(self.screen, RED, (210, 565), (1030, 565), 2)

        prompt = self.small_font.render(f"Enter your choice: {self.input_text}", True, WHITE)
        self.screen.blit(prompt, (210, 590))

        hint = self.small_font.render("Press ENTER to select.", True, RED)
        self.screen.blit(hint, (210, 620))

    def draw_output_screen(self):
        self.draw_text_box()

        title = self.title_font.render("KANJO REPORT", True, RED)
        self.screen.blit(title, (210, 115))

        self.draw_wrapped_text(
            self.output_text,
            210,
            165,
            850,
            25,
            self.small_font,
        )

        hint = self.small_font.render("Press ENTER to return to menu.", True, RED)
        self.screen.blit(hint, (210, 630))

    def run_menu_choice(self, choice):
        if choice == "1":
            return create_player(self.username)

        if choice == "2":
            return profile(self.username)

        if choice == "3":
            return garage(self.username)

        if choice == "4":
            return race_ai(self.username)

        if choice == "5":
            return repair_car(self.username)

        if choice == "6":
            return upgrade_car(self.username)

        if choice == "7":
            return upgrade_garage(self.username)

        if choice == "8":
            return claim_daily_reward(self.username)

        if choice == "9":
            return boss_race(self.username)

        if choice == "10":
            dealer_text, self.current_dealer_cars = view_dealer()
            return dealer_text

        if choice == "11":
            if not self.current_dealer_cars:
                return "View the Scrap Yard Dealer first."
            self.mode = "buy_car"
            self.input_text = ""
            return "Enter dealer car number: 1, 2, or 3"

        if choice == "12":
            return view_owned_cars(self.username)

        if choice == "13":
            self.mode = "switch_car"
            self.input_text = ""
            return "Enter the car ID you want to drive."

        if choice == "14":
            return view_world_event()

        if choice == "15":
            return view_achievements(self.username)

        if choice == "16":
            return view_stats(self.username)

        if choice == "17":
            return reputation_leaderboard()

        if choice == "18":
            return money_leaderboard()

        if choice == "19":
            return garage_leaderboard()

        if choice == "20":
            return car_power_leaderboard()

        if choice == "21":
            pygame.quit()
            sys.exit()

        return "Invalid choice."

    def handle_enter(self):
        if self.mode == "username":
            if self.input_text.strip():
                self.username = self.input_text.strip()
                self.input_text = ""
                self.mode = "menu"
            return

        if self.mode == "menu":
            result = self.run_menu_choice(self.input_text.strip())

            if self.mode in ["buy_car", "switch_car"]:
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
                self.input_text.strip()
            )
            self.input_text = ""
            self.mode = "output"
            return

        if self.mode == "switch_car":
            self.output_text = switch_active_car(
                self.username,
                self.input_text.strip()
            )
            self.input_text = ""
            self.mode = "output"
            return

        if self.mode == "output":
            self.input_text = ""
            self.mode = "menu"
            return

    def run(self):
        while True:
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
                        if self.mode != "menu":
                            self.mode = "menu"
                            self.input_text = ""

                    else:
                        if len(self.input_text) < 40:
                            self.input_text += event.unicode

            if self.mode == "username":
                self.draw_username_screen()
            elif self.mode == "menu":
                self.draw_menu_screen()
            else:
                self.draw_output_screen()

            pygame.display.flip()
            self.clock.tick(60)
