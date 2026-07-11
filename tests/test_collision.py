from __future__ import annotations

from volley.entities.ball import Ball
from volley.entities.paddle import Paddle


def test_substepped_swept_collision_catches_tunneling_case() -> None:
    paddle = Paddle(120, 200, 400)
    ball = Ball(x=260, y=230, vx=-2600, vy=0)
    events, point = ball.update(0.08, paddle, None, record_trail=False)
    assert point is None
    assert any(event.kind == "paddle" for event in events)
    assert ball.vx > 0
