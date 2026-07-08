import pygame
from ui.button import Button
from ui.text_utils import draw_wrapped_text


class OutputScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button(
                (200, 635, 220, 36),
                "Continue",
                "continue",
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
            Button(
                (440, 635, 220, 36),
                "Driver Select",
                "back_to_save",
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
        ]

    def draw(self):
        game = self.game
        game.draw_panel()

        title = game.title_font.render("KANJO REPORT", True, game.RED)
        game.screen.blit(title, (200, 95))

        draw_wrapped_text(
            game.screen,
            game.output_text,
            200,
            150,
            880,
            24,
            game.small_font,
            game.WHITE,
            600,
        )

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(game.screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "continue"
            if event.key == pygame.K_ESCAPE:
                return "back_to_save"

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
