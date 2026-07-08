import pygame
from ui.button import Button
from ui.text_utils import draw_wrapped_text


class SaveScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.make_buttons()

    def make_buttons(self):
        labels = [
            ("New Driver", "new_driver"),
            ("Load Driver", "load_driver"),
            ("View Drivers", "view_drivers"),
            ("Delete Driver", "delete_driver"),
            ("Credits", "credits"),
            ("Quit", "quit"),
        ]

        self.buttons = []
        x = 440
        y = 185
        w = 400
        h = 48
        gap = 62

        for index, (label, action) in enumerate(labels):
            self.buttons.append(
                Button(
                    (x, y + index * gap, w, h),
                    label,
                    action,
                    font=self.game.font,
                    bg_color=(15, 15, 20),
                    hover_color=(90, 10, 20),
                )
            )

    def draw(self):
        game = self.game
        game.draw_panel()

        title = game.title_font.render("DRIVER SELECT", True, game.RED)
        game.screen.blit(title, (200, 105))

        hint = game.small_font.render("Use mouse or keyboard numbers 1-6.", True, game.RED)
        game.screen.blit(hint, (200, 610))

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(game.screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: "new_driver",
                pygame.K_2: "load_driver",
                pygame.K_3: "view_drivers",
                pygame.K_4: "delete_driver",
                pygame.K_5: "credits",
                pygame.K_6: "quit",
            }

            if event.key in key_map:
                return key_map[event.key]

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
