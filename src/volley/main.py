from __future__ import annotations

import logging
from pathlib import Path

import pygame

from volley.audio import AudioManager
from volley.config import BALL_MAX_SPEED, FPS, HEIGHT, MAX_DT, VALID_TRANSITIONS, WIDTH, Difficulty, Mode, StateId
from volley.entities.ball import Ball
from volley.entities.paddle import Paddle
from volley.settings import GameSettings, load_settings, save_settings
from volley.states import (
    ControlsState,
    CountdownState,
    DifficultySelectState,
    GameOverState,
    MainMenuState,
    ModeSelectState,
    PausedState,
    PlayingState,
    SettingsState,
)
from volley.theming import get_theme

LOG = logging.getLogger(__name__)


class DemoRally:
    def __init__(self) -> None:
        self.left = Paddle(70, 222, 330)
        self.right = Paddle(WIDTH - 86, 222, 330)
        self.ball = Ball(vx=250, vy=100)

    def update(self, dt: float) -> None:
        self.left.track(self.ball.y + self.ball.size / 2, dt, 16)
        self.right.track(self.ball.y + self.ball.size / 2, dt, 16)
        _, point = self.ball.update(dt, self.left, self.right, record_trail=True)
        if point is not None:
            self.ball.reset(1 if point == 0 else -1)

    def draw(self, surface: pygame.Surface, theme) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*theme.background, 230))
        surface.blit(overlay, (0, 0))
        pygame.draw.rect(surface, (*theme.paddle, 90), self.left.rect, border_radius=3)
        pygame.draw.rect(surface, (*theme.paddle, 90), self.right.rect, border_radius=3)
        pygame.draw.rect(surface, (*theme.ball, 110), self.ball.rect, border_radius=4)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Volley")
        self.settings: GameSettings = load_settings()
        flags = pygame.RESIZABLE | (pygame.FULLSCREEN if self.settings.fullscreen else 0)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = False
        self.mode = Mode.VS_AI
        self.difficulty = (
            Difficulty(self.settings.difficulty)
            if self.settings.difficulty in {difficulty.value for difficulty in Difficulty}
            else Difficulty.PRO
        )
        self.ball_max_speed = BALL_MAX_SPEED
        self.previous_state = StateId.MAIN_MENU
        self.winner = ""
        self.final_score = ""
        self.theme = get_theme(self.settings.theme)
        self.fonts = self._load_fonts()
        asset_root = Path(__file__).resolve().parent / "assets"
        self.audio = AudioManager(asset_root, self.settings.music_volume, self.settings.sfx_volume)
        self.demo = DemoRally()
        self.playing = PlayingState(self)
        self.states = {
            StateId.MAIN_MENU: MainMenuState(self),
            StateId.MODE_SELECT: ModeSelectState(self),
            StateId.DIFFICULTY_SELECT: DifficultySelectState(self),
            StateId.COUNTDOWN: CountdownState(self),
            StateId.PLAYING: self.playing,
            StateId.PAUSED: PausedState(self),
            StateId.GAME_OVER: GameOverState(self),
            StateId.SETTINGS: SettingsState(self),
            StateId.CONTROLS: ControlsState(self),
        }
        self.state_id = StateId.MAIN_MENU
        self.state = self.states[self.state_id]
        self.state.enter()

    def _load_fonts(self) -> dict[str, pygame.font.Font]:
        return {
            "title": pygame.font.SysFont("arialblack", 76),
            "heading": pygame.font.SysFont("arialblack", 42),
            "score": pygame.font.SysFont("arialblack", 46),
            "menu": pygame.font.SysFont("arial", 30, bold=True),
            "small": pygame.font.SysFont("arial", 18),
        }

    def refresh_theme(self) -> None:
        self.theme = get_theme(self.settings.theme)

    def start_match(self) -> None:
        self.audio.start_music()
        self.playing.new_match()
        self.change_state(StateId.COUNTDOWN)

    def change_state(self, state_id: StateId) -> None:
        if state_id not in VALID_TRANSITIONS[self.state_id]:
            LOG.debug("Rejected invalid transition %s -> %s", self.state_id, state_id)
            return
        self.state.exit()
        self.state_id = state_id
        self.state = self.states[state_id]
        self.state.enter()

    def toggle_fullscreen(self) -> None:
        self.settings.fullscreen = not self.settings.fullscreen
        flags = pygame.RESIZABLE | (pygame.FULLSCREEN if self.settings.fullscreen else 0)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
        save_settings(self.settings)

    def draw_demo_background(self, screen: pygame.Surface) -> None:
        screen.fill(self.theme.background)
        self.demo.draw(screen, self.theme)

    def _present(self) -> None:
        win_w, win_h = self.screen.get_size()
        scale = min(win_w / WIDTH, win_h / HEIGHT)
        out_w, out_h = round(WIDTH * scale), round(HEIGHT * scale)
        x, y = (win_w - out_w) // 2, (win_h - out_h) // 2
        self.screen.fill((0, 0, 0))
        scaled = pygame.transform.smoothscale(self.surface, (out_w, out_h))
        self.screen.blit(scaled, (x, y))
        pygame.display.flip()

    def run(self) -> int:
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, MAX_DT)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    self.debug = not self.debug
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                else:
                    self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw(self.surface)
            self._present()
        save_settings(self.settings)
        pygame.quit()
        return 0


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    return Game().run()


if __name__ == "__main__":
    raise SystemExit(main())
