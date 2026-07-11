from __future__ import annotations

import random
from dataclasses import dataclass

from volley.config import AI_CONFIGS, HEIGHT, PADDLE_H, Difficulty
from volley.entities.ball import Ball
from volley.entities.paddle import Paddle


def predict_intercept(ball: Ball, paddle_x: float) -> float:
    if ball.vx == 0:
        return ball.y + ball.size / 2
    time = (paddle_x - (ball.x + ball.size / 2)) / ball.vx
    if time < 0:
        return HEIGHT / 2
    y = ball.y + ball.size / 2 + ball.vy * time
    span = HEIGHT - ball.size
    folded = y % (2 * span)
    if folded > span:
        folded = 2 * span - folded
    return folded


@dataclass
class AiController:
    difficulty: Difficulty
    side: str = "right"
    reaction_timer: float = 0.0
    target_y: float = HEIGHT / 2
    error: float = 0.0

    def __post_init__(self) -> None:
        self.config = AI_CONFIGS[self.difficulty]

    def reset(self) -> None:
        self.reaction_timer = 0.0
        self.target_y = HEIGHT / 2
        self.error = 0.0

    def update(self, ball: Ball, paddle: Paddle, dt: float) -> None:
        moving_toward_ai = (self.side == "right" and ball.vx > 0) or (self.side == "left" and ball.vx < 0)
        waiting_for_midline = (self.side == "right" and ball.x < 480) or (self.side == "left" and ball.x > 480)
        if self.config.waits_for_midline and waiting_for_midline:
            paddle.track(HEIGHT / 2, dt)
            return
        self.reaction_timer += dt
        if self.reaction_timer >= self.config.delay:
            if moving_toward_ai:
                self.target_y = predict_intercept(ball, paddle.x)
            else:
                self.target_y = HEIGHT / 2
            self.error = random.uniform(-self.config.error_px, self.config.error_px)
            self.reaction_timer = 0.0
        target = self.target_y + self.error
        if self.difficulty is Difficulty.LEGENDARY and moving_toward_ai:
            target += random.uniform(-PADDLE_H, PADDLE_H) * self.config.aim_variance
        paddle.speed = self.config.speed
        paddle.track(target, dt, dead_zone=5 if self.difficulty is Difficulty.LEGENDARY else 12)
