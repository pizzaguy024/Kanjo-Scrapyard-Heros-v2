import pygame
from ui.button import Button


class MenuScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.make_buttons()

    def make_buttons(self):
        self.buttons = []

        left_x = 200
        right_x = 660
        start_y = 145
        button_w = 380
        button_h = 35
        gap = 43

        for index, option in enumerate(self.game.MENU_OPTIONS, start=1):
            if index <= 11:
                x = left_x
                y = start_y + ((index - 1) * gap)
            else:
                x = right_x
                y = start_y + ((index - 12) * gap)

            self.buttons.append(
                Button(
                    (x, y, button_w, button_h),
                    option,
                    str(index),
                    font=self.game.small_font,
                    bg_color=(15, 15, 20),
                    hover_color=(90, 10, 20),
                )
            )

    def draw(self):
        game = self.game
        game.draw_panel()

        title = game.title_font.render("KANJO: SCRAP YARD HEROES V2", True, game.RED)
        game.screen.blit(title, (200, 95))

        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(game.screen)

        hint = game.small_font.render("Click a button, or use keyboard numbers.", True, game.RED)
        game.screen.blit(hint, (200, 635))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_save"

            if event.unicode and event.unicode.isdigit():
                self.game.input_text += event.unicode
                return None

            if event.key == pygame.K_RETURN:
                choice = self.game.input_text.strip()
                self.game.input_text = ""
                return choice

            if event.key == pygame.K_BACKSPACE:
                self.game.input_text = self.game.input_text[:-1]

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                return action

        return None
