import pygame
from game.icons import draw_icon


class ChoiceButton:
    def __init__(self, choice_name, rect, color, hover_color):
        self.choice_name = choice_name
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.icon_size = round(min(rect.w, rect.h) * 0.8)

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, surface, enabled=True):
        hovered = enabled and self.rect.collidepoint(pygame.mouse.get_pos())

        if not enabled:
            bg_color = tuple(c // 2 for c in self.color)
            border_color = (110, 112, 122)
        elif hovered:
            bg_color = self.hover_color
            border_color = (255, 255, 255)
        else:
            bg_color = self.color
            border_color = (230, 230, 235)

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)

        # Icon grows slightly on hover
        size = round(self.icon_size * 1.08) if hovered else self.icon_size
        draw_icon(surface, self.choice_name, self.rect.center, size)