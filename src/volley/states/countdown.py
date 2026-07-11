from __future__ import annotations

import pygame

from volley.config import StateId
from volley.states.base import GameState
from volley.ui.text_fx import draw_center_text


class CountdownState(GameState):
    state_id = StateId.COUNTDOWN

    def enter(self) -> None:
        self.timer = 0.0
        self.last_mark = ""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ctx.change_state(StateId.MAIN_MENU)

    def update(self, dt: float) -> None:
        self.timer += dt
        label = self.label()
        if label != self.last_mark and label:
            self.ctx.audio.play("tick")
            self.last_mark = label
        if self.timer >= 3.6:
            self.ctx.change_state(StateId.PLAYING)

    def label(self) -> str:
        if self.timer < 0.8:
            return "3"
        if self.timer < 1.6:
            return "2"
        if self.timer < 2.4:
            return "1"
        if self.timer < 3.2:
            return "GO"
        return ""

    def draw(self, screen: pygame.Surface) -> None:
        self.ctx.playing.draw(screen)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 95))
        screen.blit(overlay, (0, 0))
        draw_center_text(screen, self.ctx.fonts["title"], self.label(), self.ctx.theme.accent, (480, 260))
