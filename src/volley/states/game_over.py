from __future__ import annotations

import pygame

from volley.config import Mode, StateId
from volley.settings import load_high_scores
from volley.states.base import GameState
from volley.ui.menu import Menu, MenuChoice
from volley.ui.text_fx import draw_center_text


class GameOverState(GameState):
    state_id = StateId.GAME_OVER

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.menu = Menu([MenuChoice("Rematch", "rematch"), MenuChoice("Main Menu", "menu")], (480, 360))

    def enter(self) -> None:
        self.ctx.audio.play("win")
        self.ctx.playing.particles.burst((480, 180), self.ctx.theme.accent2, 80, 400)

    def handle_event(self, event: pygame.event.Event) -> None:
        choice = self.menu.handle_event(event)
        if choice == "rematch":
            self.ctx.start_match()
        elif choice == "menu":
            self.ctx.change_state(StateId.MAIN_MENU)

    def update(self, dt: float) -> None:
        self.ctx.playing.particles.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.ctx.theme.background)
        self.ctx.playing.particles.draw(screen)
        draw_center_text(screen, self.ctx.fonts["heading"], self.ctx.winner, self.ctx.theme.text, (480, 142))
        draw_center_text(screen, self.ctx.fonts["menu"], self.ctx.final_score, self.ctx.theme.accent, (480, 218))
        self.menu.center = (480, 360)
        if self.ctx.mode is Mode.RALLY:
            draw_center_text(screen, self.ctx.fonts["small"], "Top Rally Scores", self.ctx.theme.text, (480, 268))
            for idx, score in enumerate(load_high_scores(), start=1):
                line = f"{idx}. Rally {score.rally} | Max speed {score.max_speed}"
                draw_center_text(
                    screen,
                    self.ctx.fonts["small"],
                    line,
                    self.ctx.theme.muted,
                    (480, 292 + idx * 22),
                )
            self.menu.center = (480, 452)
        self.menu.draw(
            screen,
            self.ctx.fonts["menu"],
            self.ctx.fonts["small"],
            self.ctx.theme.text,
            self.ctx.theme.accent,
            self.ctx.theme.muted,
        )
