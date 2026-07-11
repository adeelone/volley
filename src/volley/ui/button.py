from __future__ import annotations

import pygame


def draw_toggle(
    surface: pygame.Surface,
    rect: pygame.Rect,
    on: bool,
    accent: tuple[int, int, int],
    muted: tuple[int, int, int],
) -> None:
    pygame.draw.rect(surface, accent if on else muted, rect, border_radius=rect.height // 2)
    knob_x = rect.right - rect.height + 3 if on else rect.x + 3
    pygame.draw.circle(surface, (255, 255, 255), (knob_x + rect.height // 2 - 3, rect.centery), rect.height // 2 - 5)
