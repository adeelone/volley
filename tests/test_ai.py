from __future__ import annotations

from volley.ai import AiController, predict_intercept
from volley.config import HEIGHT, Difficulty
from volley.entities.ball import Ball
from volley.entities.paddle import Paddle


def test_predict_intercept_accounts_for_wall_bounce() -> None:
    ball = Ball(x=100, y=30, vx=200, vy=-180)
    y = predict_intercept(ball, 700)
    assert 0 <= y <= HEIGHT
    assert abs(y - 496.7) < 4


def test_rookie_waits_for_midline() -> None:
    ball = Ball(x=200, y=80, vx=250, vy=0)
    paddle = Paddle(900, 250, 400)
    ai = AiController(Difficulty.ROOKIE)
    before = paddle.y
    ai.update(ball, paddle, 0.2)
    assert paddle.y != before
    assert ai.config.delay > 0
    assert ai.config.waits_for_midline


def test_pro_updates_target_and_moves_paddle() -> None:
    ball = Ball(x=500, y=120, vx=260, vy=40)
    paddle = Paddle(900, 250, 400)
    ai = AiController(Difficulty.PRO)
    before = paddle.y
    ai.update(ball, paddle, 0.2)
    assert ai.target_y != HEIGHT / 2
    assert paddle.y != before
    ai.reset()
    assert ai.target_y == HEIGHT / 2
    assert ai.error == 0


def test_legendary_adjusts_speed_when_ball_moves_toward_it() -> None:
    ball = Ball(x=700, y=120, vx=260, vy=40)
    paddle = Paddle(900, 250, 400)
    ai = AiController(Difficulty.LEGENDARY)
    ai.update(ball, paddle, 0.1)
    assert paddle.speed == ai.config.speed


def test_legendary_has_zero_reaction_delay() -> None:
    assert AiController(Difficulty.LEGENDARY).config.delay == 0
