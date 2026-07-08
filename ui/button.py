import pygame


class Button:
    def __init__(
        self,
        rect,
        text,
        action=None,
        font=None,
        text_color=(235, 235, 235),
        bg_color=(20, 20, 25),
        hover_color=(90, 10, 20),
        border_color=(220, 40, 50),
        disabled=False,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.disabled = disabled
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos) and not self.disabled

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.bg_color

        if self.disabled:
            color = (35, 35, 35)

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=8)

        if self.font:
            rendered = self.font.render(self.text, True, self.text_color)
            text_rect = rendered.get_rect(center=self.rect.center)
            surface.blit(rendered, text_rect)

    def handle_event(self, event):
        if self.disabled:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return self.action

        return None
