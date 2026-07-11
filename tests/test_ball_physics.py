from __future__ import annotations

import math

from volley.config import BALL_MAX_SPEED, HEIGHT
from volley.entities.ball import Ball
from volley.entities.paddle import Paddle


def test_wall_bounce_uses_height_and_reflects() -> None:
    ball = Ball(y=HEIGHT - 16, vx=0, vy=500)
    events, point = ball.update(0.05, None, None, record_trail=False)
    assert point is None
    assert ball.vy < 0
    assert any(event.kind == "wall" for event in events)


def test_speed_caps_after_repeated_paddle_hits() -> None:
    paddle = Paddle(20, 200, 400)
    ball = Ball(x=30, y=230, vx=-400, vy=0)
    for _ in range(80):
        ball.hit_paddle(paddle, 1)
    assert ball.speed <= BALL_MAX_SPEED


def test_edge_hit_creates_sharper_angle_than_center_hit() -> None:
    paddle = Paddle(20, 200, 400)
    center = Ball(x=30, y=paddle.center_y - 7, vx=-400, vy=0)
    edge = Ball(x=30, y=paddle.y + 2, vx=-400, vy=0)
    center.hit_paddle(paddle, 1)
    edge.hit_paddle(paddle, 1)
    center_angle = abs(math.atan2(center.vy, center.vx))
    edge_angle = abs(math.atan2(edge.vy, edge.vx))
    assert edge_angle > center_angle
