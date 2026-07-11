from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from volley.states.playing import PlayingState


class Dummy:
    def __init__(self) -> None:
        from volley.config import Difficulty, Mode
        from volley.settings import GameSettings
        from volley.theming import get_theme

        self.difficulty = Difficulty.PRO
        self.mode = Mode.TWO_PLAYER
        self.settings = GameSettings(win_score=11)
        self.theme = get_theme("Neon")


def test_win_by_two_rule() -> None:
    state = PlayingState(Dummy())
    state.score = [11, 10]
    assert not state.is_match_over()
    state.score = [12, 10]
    assert state.is_match_over()
