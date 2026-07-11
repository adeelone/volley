from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from volley.settings import GameSettings, RallyScore, load_high_scores, load_settings, save_high_score, save_settings


def local_temp_path(name: str) -> Path:
    root = Path.cwd() / ".pytest-local"
    root.mkdir(exist_ok=True)
    return root / f"{name}-{uuid4().hex}.json"


def test_settings_round_trip() -> None:
    path = local_temp_path("settings")
    settings = GameSettings(theme="Sunset", music_volume=0.2, sfx_volume=0.4, win_score=15)
    settings.keys.p1_up = 97
    settings.keys.p2_down = 98
    save_settings(settings, path)
    loaded = load_settings(path)
    assert loaded.theme == "Sunset"
    assert loaded.music_volume == 0.2
    assert loaded.sfx_volume == 0.4
    assert loaded.win_score == 15
    assert loaded.keys.p1_up == 97
    assert loaded.keys.p2_down == 98


def test_corrupt_settings_fall_back() -> None:
    path = local_temp_path("corrupt-settings")
    path.write_text("{not json", encoding="utf-8")
    loaded = load_settings(path)
    assert loaded == GameSettings()


def test_high_scores_keep_top_five() -> None:
    path = local_temp_path("scores")
    for idx in range(8):
        save_high_score(RallyScore(idx, idx * 10), path)
    scores = load_high_scores(path)
    assert len(scores) == 5
    assert scores[0].rally == 7
