from __future__ import annotations

import pygame

from volley.config import Mode, StateId
from volley.states.base import GameState
from volley.ui.menu import Menu, MenuChoice
from volley.ui.text_fx import draw_center_text


class ModeSelectState(GameState):
    state_id = StateId.MODE_SELECT

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.menu = Menu(
            [
                MenuChoice(Mode.VS_AI.value, Mode.VS_AI.value, "Solo match against a tuned opponent."),
                MenuChoice(Mode.TWO_PLAYER.value, Mode.TWO_PLAYER.value, "Local W/S vs Up/Down match."),
                MenuChoice(Mode.RALLY.value, Mode.RALLY.value, "One paddle. Longest rally wins."),
                MenuChoice("Back", "back"),
            ],
            (480, 295),
            66,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ctx.change_state(StateId.MAIN_MENU)
        choice = self.menu.handle_event(event)
        if choice == Mode.VS_AI.value:
            self.ctx.mode = Mode.VS_AI
            self.ctx.change_state(StateId.DIFFICULTY_SELECT)
        elif choice == Mode.TWO_PLAYER.value:
            self.ctx.mode = Mode.TWO_PLAYER
            self.ctx.start_match()
        elif choice == Mode.RALLY.value:
            self.ctx.mode = Mode.RALLY
            self.ctx.start_match()
        elif choice == "back":
            self.ctx.change_state(StateId.MAIN_MENU)

    def update(self, dt: float) -> None:
        self.ctx.demo.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.ctx.draw_demo_background(screen)
        draw_center_text(screen, self.ctx.fonts["heading"], "Choose Mode", self.ctx.theme.text, (480, 96))
        self.menu.draw(
            screen, self.ctx.fonts["menu"], self.ctx.fonts["small"], self.ctx.theme.text, self.ctx.theme.accent, self.ctx.theme.muted
        )
