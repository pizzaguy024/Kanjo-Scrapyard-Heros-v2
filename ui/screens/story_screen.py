import pygame
from ui.button import Button
from ui.text_utils import draw_wrapped_text


class StoryScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button(
                (200, 635, 220, 36),
                "Continue",
                "continue_story",
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
            Button(
                (440, 635, 220, 36),
                "Skip",
                "skip_story",
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
        ]

    def draw(self):
        game = self.game
        game.draw_panel()

        title = game.title_font.render("THE BEGINNING", True, game.RED)
        game.screen.blit(title, (200, 105))

        draw_wrapped_text(
            game.screen,
            game.story_visible_text,
            200,
            170,
            880,
            30,
            game.font,
            game.WHITE,
            575,
        )

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(game.screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "continue_story"
            if event.key == pygame.K_ESCAPE:
                return "back_to_save"

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
