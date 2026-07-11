from __future__ import annotations

import pygame

from volley.config import StateId
from volley.states.base import GameState
from volley.ui.menu import Menu, MenuChoice
from volley.ui.text_fx import draw_center_text


class PausedState(GameState):
    state_id = StateId.PAUSED

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.menu = Menu(
            [
                MenuChoice("Resume", "resume"),
                MenuChoice("Restart", "restart"),
                MenuChoice("Settings", "settings"),
                MenuChoice("Quit to Menu", "menu"),
            ],
            (480, 308),
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ctx.change_state(StateId.PLAYING)
        choice = self.menu.handle_event(event)
        if choice == "resume":
            self.ctx.change_state(StateId.PLAYING)
        elif choice == "restart":
            self.ctx.start_match()
        elif choice == "settings":
            self.ctx.previous_state = StateId.PAUSED
            self.ctx.change_state(StateId.SETTINGS)
        elif choice == "menu":
            self.ctx.change_state(StateId.MAIN_MENU)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        self.ctx.playing.draw(screen)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        draw_center_text(screen, self.ctx.fonts["heading"], "Paused", self.ctx.theme.text, (480, 130))
        self.menu.draw(
            screen,
            self.ctx.fonts["menu"],
            self.ctx.fonts["small"],
            self.ctx.theme.text,
            self.ctx.theme.accent,
            self.ctx.theme.muted,
        )
