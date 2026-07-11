from __future__ import annotations

import pygame

from volley.config import StateId
from volley.states.base import GameState
from volley.ui.text_fx import draw_center_text


class ControlsState(GameState):
    state_id = StateId.CONTROLS

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            target = self.ctx.previous_state if self.ctx.previous_state in (StateId.MAIN_MENU, StateId.PAUSED) else StateId.MAIN_MENU
            self.ctx.change_state(target)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.ctx.theme.background)
        draw_center_text(screen, self.ctx.fonts["heading"], "Controls", self.ctx.theme.text, (480, 78))
        labels = self.ctx.settings.keys.labels()
        lines = [
            f"P1 Up / Down: {labels['p1_up']} / {labels['p1_down']}",
            f"P2 Up / Down: {labels['p2_up']} / {labels['p2_down']}",
            "Menus: Arrow keys or W/S, Enter/Space, mouse hover/click",
            "Esc: pause/back   F3: debug overlay   F11: fullscreen",
            "Press Enter or Esc to return",
        ]
        for idx, line in enumerate(lines):
            draw_center_text(
                screen,
                self.ctx.fonts["menu" if idx < 2 else "small"],
                line,
                self.ctx.theme.accent if idx < 2 else self.ctx.theme.text,
                (480, 165 + idx * 58),
            )
