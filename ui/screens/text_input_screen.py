import pygame
from ui.button import Button
from ui.text_utils import draw_wrapped_text


class TextInputScreen:
    def __init__(self, game):
        self.game = game
        self.title = "TEXT INPUT"
        self.body = ""
        self.label = "Input"
        self.confirm_action = "confirm"
        self.buttons = []
        self.make_buttons()

    def configure(self, title, body, label, confirm_action):
        self.title = title
        self.body = body
        self.label = label
        self.confirm_action = confirm_action
        self.game.input_text = ""
        self.make_buttons()

    def make_buttons(self):
        self.buttons = [
            Button(
                (200, 635, 180, 36),
                "Confirm",
                self.confirm_action,
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
            Button(
                (400, 635, 180, 36),
                "Back",
                "back_to_save",
                font=self.game.small_font,
                bg_color=(15, 15, 20),
                hover_color=(90, 10, 20),
            ),
        ]

    def draw_input_box(self):
        game = self.game

        input_box = pygame.Surface((880, 45), pygame.SRCALPHA)
        input_box.fill(game.INPUT_BG)
        game.screen.blit(input_box, (200, 570))
        pygame.draw.rect(game.screen, game.RED, (200, 570, 880, 45), 2)

        display_text = game.input_text
        if game.cursor_visible:
            display_text += "|"

        rendered = game.font.render(f"{self.label}: {display_text}", True, game.WHITE)
        game.screen.blit(rendered, (215, 579))

    def draw(self):
        game = self.game
        game.draw_panel()

        title = game.title_font.render(self.title, True, game.RED)
        game.screen.blit(title, (200, 105))

        draw_wrapped_text(
            game.screen,
            self.body,
            200,
            165,
            880,
            27,
            game.small_font,
            game.WHITE,
            535,
        )

        self.draw_input_box()

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(game.screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.confirm_action
            if event.key == pygame.K_ESCAPE:
                return "back_to_save"
            if event.key == pygame.K_BACKSPACE:
                self.game.input_text = self.game.input_text[:-1]
                return None
            if len(self.game.input_text) < 40 and event.unicode:
                self.game.input_text += event.unicode

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
