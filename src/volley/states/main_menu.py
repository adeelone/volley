from __future__ import annotations

import pygame

from volley.config import StateId
from volley.states.base import GameState
from volley.ui.menu import Menu, MenuChoice
from volley.ui.text_fx import outlined_text, pulse_scale


class MainMenuState(GameState):
    state_id = StateId.MAIN_MENU

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.menu = Menu(
            [
                MenuChoice("Play", "play"),
                MenuChoice("Settings", "settings"),
                MenuChoice("Controls", "controls"),
                MenuChoice("Quit", "quit"),
            ],
            (480, 335),
        )
        self.t = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        previous_selection = self.menu.selected
        choice = self.menu.handle_event(event)
        if choice is None and self.menu.selected != previous_selection:
            self.ctx.audio.play("menu")
        if choice:
            self.ctx.audio.play("confirm")
        if choice == "play":
            self.ctx.change_state(StateId.MODE_SELECT)
        elif choice == "settings":
            self.ctx.previous_state = StateId.MAIN_MENU
            self.ctx.change_state(StateId.SETTINGS)
        elif choice == "controls":
            self.ctx.previous_state = StateId.MAIN_MENU
            self.ctx.change_state(StateId.CONTROLS)
        elif choice == "quit":
            self.ctx.running = False

    def update(self, dt: float) -> None:
        self.t += dt
        self.ctx.demo.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        theme = self.ctx.theme
        self.ctx.draw_demo_background(screen)
        title = outlined_text(self.ctx.fonts["title"], "VOLLEY", theme.accent, (0, 0, 0))
        scale = pulse_scale(self.t)
        title = pygame.transform.smoothscale(
            title, (round(title.get_width() * scale), round(title.get_height() * scale))
        )
        screen.blit(title, title.get_rect(center=(480, 128)))
        self.menu.draw(screen, self.ctx.fonts["menu"], self.ctx.fonts["small"], theme.text, theme.accent, theme.muted)
