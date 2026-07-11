from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

WIDTH = 960
HEIGHT = 540
FPS = 60
MAX_DT = 4 / FPS
PADDLE_W = 16
PADDLE_H = 96
BALL_SIZE = 14
HUMAN_PADDLE_SPEED = 420.0
BALL_START_SPEED = 315.0
BALL_SPEEDUP = 1.055
BALL_MAX_SPEED = 760.0
RALLY_MAX_SPEED = 860.0
WIN_SCORE_DEFAULT = 11


class Mode(StrEnum):
    VS_AI = "1 Player vs AI"
    TWO_PLAYER = "2 Player"
    RALLY = "Rally Survival"


class Difficulty(StrEnum):
    ROOKIE = "Rookie"
    PRO = "Pro"
    LEGENDARY = "Legendary"


class StateId(StrEnum):
    MAIN_MENU = "main_menu"
    MODE_SELECT = "mode_select"
    DIFFICULTY_SELECT = "difficulty_select"
    COUNTDOWN = "countdown"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    CONTROLS = "controls"


@dataclass(frozen=True)
class AiConfig:
    delay: float
    speed: float
    error_px: float
    waits_for_midline: bool
    aim_variance: float


AI_CONFIGS = {
    Difficulty.ROOKIE: AiConfig(0.28, 300.0, 46.0, True, 0.1),
    Difficulty.PRO: AiConfig(0.08, HUMAN_PADDLE_SPEED, 12.0, False, 0.28),
    Difficulty.LEGENDARY: AiConfig(0.0, 510.0, 0.0, False, 0.55),
}


VALID_TRANSITIONS: dict[StateId, set[StateId]] = {
    StateId.MAIN_MENU: {StateId.MODE_SELECT, StateId.SETTINGS, StateId.CONTROLS},
    StateId.MODE_SELECT: {StateId.MAIN_MENU, StateId.DIFFICULTY_SELECT, StateId.COUNTDOWN},
    StateId.DIFFICULTY_SELECT: {StateId.MODE_SELECT, StateId.COUNTDOWN},
    StateId.COUNTDOWN: {StateId.PLAYING, StateId.MAIN_MENU},
    StateId.PLAYING: {StateId.PAUSED, StateId.COUNTDOWN, StateId.GAME_OVER, StateId.MAIN_MENU},
    StateId.PAUSED: {StateId.PLAYING, StateId.COUNTDOWN, StateId.SETTINGS, StateId.MAIN_MENU},
    StateId.SETTINGS: {StateId.MAIN_MENU, StateId.PAUSED},
    StateId.CONTROLS: {StateId.MAIN_MENU, StateId.PAUSED},
    StateId.GAME_OVER: {StateId.MAIN_MENU, StateId.COUNTDOWN},
}
