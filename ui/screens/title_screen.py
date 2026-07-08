import pygame
from ui.button import Button


class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button(
                (465, 420, 350, 55),
                "PRESS START",
                "start",
                font=self.game.font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            )
        ]

    def draw(self):
        game = self.game
        screen = game.screen

        overlay = pygame.Surface((game.WIDTH, game.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        screen.blit(overlay, (0, 0))

        title_1 = game.logo_font.render("KANJO", True, game.RED)
        title_2 = game.title_font.render("SCRAP YARD HEROES", True, game.WHITE)

        screen.blit(title_1, (game.WIDTH // 2 - title_1.get_width() // 2, 230))
        screen.blit(title_2, (game.WIDTH // 2 - title_2.get_width() // 2, 300))

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        tagline = game.small_font.render("Every legend starts as scrap.", True, game.RED)
        screen.blit(tagline, (game.WIDTH // 2 - tagline.get_width() // 2, 495))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return "start"

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
