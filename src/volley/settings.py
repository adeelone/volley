from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import pygame
from platformdirs import user_config_dir

from volley.config import WIN_SCORE_DEFAULT, Difficulty

LOG = logging.getLogger(__name__)
APP_NAME = "Volley"


@dataclass
class KeyBindings:
    p1_up: int = pygame.K_w
    p1_down: int = pygame.K_s
    p2_up: int = pygame.K_UP
    p2_down: int = pygame.K_DOWN

    def labels(self) -> dict[str, str]:
        return {k: pygame.key.name(v).upper() for k, v in asdict(self).items()}


@dataclass
class GameSettings:
    music_volume: float = 0.35
    sfx_volume: float = 0.7
    theme: str = "Neon"
    reduce_motion: bool = False
    ball_trail: bool = True
    win_score: int = WIN_SCORE_DEFAULT
    difficulty: str = Difficulty.PRO.value
    serve_random: bool = True
    fullscreen: bool = False
    keys: KeyBindings = field(default_factory=KeyBindings)


@dataclass
class RallyScore:
    rally: int
    max_speed: int


def config_dir() -> Path:
    path = Path(user_config_dir(APP_NAME, appauthor=False))
    path.mkdir(parents=True, exist_ok=True)
    return path


def settings_path() -> Path:
    return config_dir() / "settings.json"


def scores_path() -> Path:
    return config_dir() / "high_scores.json"


def _clamp_volume(value: Any, default: float) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def settings_from_dict(data: dict[str, Any]) -> GameSettings:
    defaults = GameSettings()
    keys_raw = data.get("keys", {})
    keys = KeyBindings(**{k: int(v) for k, v in keys_raw.items() if hasattr(defaults.keys, k)})
    return GameSettings(
        music_volume=_clamp_volume(data.get("music_volume"), defaults.music_volume),
        sfx_volume=_clamp_volume(data.get("sfx_volume"), defaults.sfx_volume),
        theme=str(data.get("theme", defaults.theme)),
        reduce_motion=bool(data.get("reduce_motion", defaults.reduce_motion)),
        ball_trail=bool(data.get("ball_trail", defaults.ball_trail)),
        win_score=max(3, min(31, int(data.get("win_score", defaults.win_score)))),
        difficulty=str(data.get("difficulty", defaults.difficulty)),
        serve_random=bool(data.get("serve_random", defaults.serve_random)),
        fullscreen=bool(data.get("fullscreen", defaults.fullscreen)),
        keys=keys,
    )


def load_settings(path: Path | None = None) -> GameSettings:
    path = path or settings_path()
    try:
        return settings_from_dict(json.loads(path.read_text(encoding="utf-8")))
    except FileNotFoundError:
        return GameSettings()
    except Exception as exc:
        LOG.warning("Falling back to default settings after load failure: %s", exc)
        return GameSettings()


def save_settings(settings: GameSettings, path: Path | None = None) -> None:
    path = path or settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(settings)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_high_scores(path: Path | None = None) -> list[RallyScore]:
    path = path or scores_path()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [RallyScore(int(item["rally"]), int(item["max_speed"])) for item in raw][:5]
    except FileNotFoundError:
        return []
    except Exception as exc:
        LOG.warning("Ignoring corrupt high score file: %s", exc)
        return []


def save_high_score(score: RallyScore, path: Path | None = None) -> list[RallyScore]:
    path = path or scores_path()
    scores = load_high_scores(path)
    scores.append(score)
    scores.sort(key=lambda item: (item.rally, item.max_speed), reverse=True)
    scores = scores[:5]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(item) for item in scores], indent=2), encoding="utf-8")
    return scores
