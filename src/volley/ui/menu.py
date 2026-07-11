from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import pygame


@dataclass
class MenuChoice:
    label: str
    value: str
    description: str = ""


class Menu:
    def __init__(self, choices: Sequence[MenuChoice], center: tuple[int, int], spacing: int = 54) -> None:
        self.choices = list(choices)
        self.center = center
        self.spacing = spacing
        self.selected = 0
        self.rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.choices)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.choices)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.choices[self.selected].value
        elif event.type == pygame.MOUSEMOTION:
            for idx, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = idx
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = idx
                    return self.choices[idx].value
        return None

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        small: pygame.font.Font,
        text: tuple[int, int, int],
        accent: tuple[int, int, int],
        muted: tuple[int, int, int],
    ) -> None:
        self.rects.clear()
        start_y = self.center[1] - (len(self.choices) - 1) * self.spacing // 2
        for idx, choice in enumerate(self.choices):
            color = accent if idx == self.selected else text
            label = font.render(choice.label, True, color)
            rect = label.get_rect(center=(self.center[0], start_y + idx * self.spacing))
            pad = rect.inflate(42, 18)
            self.rects.append(pad)
            if idx == self.selected:
                pygame.draw.rect(surface, (*accent, 45), pad, border_radius=7)
                pygame.draw.rect(surface, accent, pad, 2, border_radius=7)
            surface.blit(label, rect)
            if choice.description:
                desc = small.render(choice.description, True, muted)
                surface.blit(desc, desc.get_rect(midtop=(self.center[0], rect.bottom + 4)))
