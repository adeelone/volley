from __future__ import annotations

from volley.config import VALID_TRANSITIONS, StateId


def test_declared_transitions_cover_requested_flow() -> None:
    assert StateId.MODE_SELECT in VALID_TRANSITIONS[StateId.MAIN_MENU]
    assert StateId.DIFFICULTY_SELECT in VALID_TRANSITIONS[StateId.MODE_SELECT]
    assert StateId.COUNTDOWN in VALID_TRANSITIONS[StateId.DIFFICULTY_SELECT]
    assert StateId.PLAYING in VALID_TRANSITIONS[StateId.COUNTDOWN]
    assert StateId.PAUSED in VALID_TRANSITIONS[StateId.PLAYING]
    assert StateId.GAME_OVER in VALID_TRANSITIONS[StateId.PLAYING]
    assert StateId.MAIN_MENU in VALID_TRANSITIONS[StateId.GAME_OVER]


def test_invalid_transition_is_not_declared() -> None:
    assert StateId.GAME_OVER not in VALID_TRANSITIONS[StateId.MAIN_MENU]
