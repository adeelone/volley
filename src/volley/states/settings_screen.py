from __future__ import annotations

import pygame

from volley.config import StateId
from volley.settings import save_settings
from volley.states.base import GameState
from volley.theming import THEMES
from volley.ui.button import draw_toggle
from volley.ui.text_fx import draw_center_text


class SettingsState(GameState):
    state_id = StateId.SETTINGS

    rows = ["music", "sfx", "theme", "motion", "trail", "score", "keys", "back"]

    def enter(self) -> None:
        self.selected = 0
        self.rebinding: str | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.rebinding and event.type == pygame.KEYDOWN:
            used = {k: v for k, v in vars(self.ctx.settings.keys).items() if k != self.rebinding}
            if event.key not in used.values():
                setattr(self.ctx.settings.keys, self.rebinding, event.key)
                save_settings(self.ctx.settings)
            self.rebinding = None
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._back()
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.rows)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.rows)
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
            self.adjust(-1 if event.key == pygame.K_LEFT else 1)

    def adjust(self, direction: int) -> None:
        row = self.rows[self.selected]
        s = self.ctx.settings
        if row == "music":
            s.music_volume = max(0, min(1, s.music_volume + 0.05 * direction))
        elif row == "sfx":
            s.sfx_volume = max(0, min(1, s.sfx_volume + 0.05 * direction))
        elif row == "theme":
            names = list(THEMES)
            s.theme = names[(names.index(s.theme) + direction) % len(names)] if s.theme in names else names[0]
            self.ctx.refresh_theme()
        elif row == "motion":
            s.reduce_motion = not s.reduce_motion
        elif row == "trail":
            s.ball_trail = not s.ball_trail
        elif row == "score":
            s.win_score = max(3, min(31, s.win_score + direction))
        elif row == "keys":
            self.rebinding = "p1_up"
        elif row == "back":
            self._back()
        self.ctx.audio.set_volumes(s.music_volume, s.sfx_volume)
        save_settings(s)

    def _back(self) -> None:
        target = (
            self.ctx.previous_state
            if self.ctx.previous_state in (StateId.MAIN_MENU, StateId.PAUSED)
            else StateId.MAIN_MENU
        )
        self.ctx.change_state(target)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.ctx.theme.background)
        draw_center_text(screen, self.ctx.fonts["heading"], "Settings", self.ctx.theme.text, (480, 70))
        labels = [
            f"Music Volume  {self.ctx.settings.music_volume:.0%}",
            f"SFX Volume  {self.ctx.settings.sfx_volume:.0%}",
            f"Theme  {self.ctx.settings.theme}",
            "Reduce Motion",
            "Ball Trail",
            f"Win Score  {self.ctx.settings.win_score}",
            "Rebind P1 Up",
            "Back",
        ]
        if self.rebinding:
            draw_center_text(
                screen,
                self.ctx.fonts["small"],
                "Press a replacement key. Existing bindings are rejected.",
                self.ctx.theme.accent,
                (480, 480),
            )
        for idx, label in enumerate(labels):
            y = 135 + idx * 44
            color = self.ctx.theme.accent if idx == self.selected else self.ctx.theme.text
            draw_center_text(screen, self.ctx.fonts["menu"], label, color, (455, y))
            if self.rows[idx] == "motion":
                draw_toggle(
                    screen,
                    pygame.Rect(680, y - 14, 54, 28),
                    self.ctx.settings.reduce_motion,
                    self.ctx.theme.accent,
                    self.ctx.theme.muted,
                )
            if self.rows[idx] == "trail":
                draw_toggle(
                    screen,
                    pygame.Rect(680, y - 14, 54, 28),
                    self.ctx.settings.ball_trail,
                    self.ctx.theme.accent,
                    self.ctx.theme.muted,
                )
