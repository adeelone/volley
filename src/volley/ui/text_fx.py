from __future__ import annotations

import math

import pygame


def outlined_text(
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    outline: tuple[int, int, int],
) -> pygame.Surface:
    base = font.render(text, True, color)
    surf = pygame.Surface((base.get_width() + 6, base.get_height() + 6), pygame.SRCALPHA)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        surf.blit(font.render(text, True, outline), (3 + dx, 3 + dy))
    surf.blit(base, (3, 3))
    return surf


def pulse_scale(t: float, amount: float = 0.05) -> float:
    return 1.0 + math.sin(t * 3.0) * amount


def draw_center_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    pos: tuple[int, int],
) -> None:
    img = font.render(text, True, color)
    surface.blit(img, img.get_rect(center=pos))
