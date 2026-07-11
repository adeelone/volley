from __future__ import annotations

import pygame

from volley.config import Difficulty, StateId
from volley.states.base import GameState
from volley.ui.menu import Menu, MenuChoice
from volley.ui.text_fx import draw_center_text


class DifficultySelectState(GameState):
    state_id = StateId.DIFFICULTY_SELECT

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.menu = Menu(
            [
                MenuChoice(Difficulty.ROOKIE.value, Difficulty.ROOKIE.value, "Delayed reactions and real mistakes."),
                MenuChoice(Difficulty.PRO.value, Difficulty.PRO.value, "Trajectory prediction with human-like correction."),
                MenuChoice(Difficulty.LEGENDARY.value, Difficulty.LEGENDARY.value, "Precise, fast, and aggressive angles."),
                MenuChoice("Back", "back"),
            ],
            (480, 295),
            66,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ctx.change_state(StateId.MODE_SELECT)
        choice = self.menu.handle_event(event)
        if choice in {item.value for item in Difficulty}:
            self.ctx.difficulty = Difficulty(choice)
            self.ctx.settings.difficulty = choice
            self.ctx.start_match()
        elif choice == "back":
            self.ctx.change_state(StateId.MODE_SELECT)

    def update(self, dt: float) -> None:
        self.ctx.demo.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.ctx.draw_demo_background(screen)
        draw_center_text(screen, self.ctx.fonts["heading"], "AI Difficulty", self.ctx.theme.text, (480, 96))
        self.menu.draw(
            screen, self.ctx.fonts["menu"], self.ctx.fonts["small"], self.ctx.theme.text, self.ctx.theme.accent, self.ctx.theme.muted
        )
