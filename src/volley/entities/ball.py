from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import pygame

from volley.config import BALL_MAX_SPEED, BALL_SIZE, BALL_SPEEDUP, HEIGHT, WIDTH
from volley.entities.paddle import Paddle


@dataclass
class CollisionEvent:
    kind: str
    speed: float
    pos: tuple[float, float]


@dataclass
class Ball:
    x: float = WIDTH / 2 - BALL_SIZE / 2
    y: float = HEIGHT / 2 - BALL_SIZE / 2
    vx: float = 315.0
    vy: float = 120.0
    size: int = BALL_SIZE
    max_speed: float = BALL_MAX_SPEED
    trail: list[tuple[float, float, float]] = field(default_factory=list)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.size, self.size)

    @property
    def center(self) -> tuple[float, float]:
        return self.x + self.size / 2, self.y + self.size / 2

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vy)

    def reset(self, direction: int = 1, randomize: bool = True) -> None:
        self.x = WIDTH / 2 - self.size / 2
        self.y = HEIGHT / 2 - self.size / 2
        angle = random.uniform(-0.45, 0.45) if randomize else 0.22
        speed = 315.0
        self.vx = direction * speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.trail.clear()

    def set_velocity_from_angle(self, direction: int, angle: float, speed: float | None = None) -> None:
        speed = min(speed if speed is not None else self.speed, self.max_speed)
        self.vx = direction * speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def hit_paddle(self, paddle: Paddle, direction: int) -> CollisionEvent:
        relative = ((self.y + self.size / 2) - paddle.center_y) / (paddle.height / 2)
        relative = max(-1.0, min(1.0, relative))
        max_angle = math.radians(62)
        new_speed = min(self.speed * BALL_SPEEDUP, self.max_speed)
        self.set_velocity_from_angle(direction, relative * max_angle, new_speed)
        if direction > 0:
            self.x = paddle.x + paddle.width + 0.5
        else:
            self.x = paddle.x - self.size - 0.5
        return CollisionEvent("paddle", self.speed, self.center)

    def update(
        self,
        dt: float,
        left: Paddle | None,
        right: Paddle | None,
        record_trail: bool = True,
    ) -> tuple[list[CollisionEvent], int | None]:
        events: list[CollisionEvent] = []
        if record_trail:
            self.trail.append((self.x, self.y, 0.3))
            self.trail = [(x, y, age - dt) for x, y, age in self.trail if age - dt > 0]
        distance = max(abs(self.vx * dt), abs(self.vy * dt))
        steps = max(1, math.ceil(distance / (self.size * 0.45)))
        step_dt = dt / steps
        for _ in range(steps):
            old = self.rect
            self.x += self.vx * step_dt
            self.y += self.vy * step_dt
            if self.y <= 0:
                self.y = 0
                self.vy = abs(self.vy)
                events.append(CollisionEvent("wall", self.speed, self.center))
            elif self.y + self.size >= HEIGHT:
                self.y = HEIGHT - self.size
                self.vy = -abs(self.vy)
                events.append(CollisionEvent("wall", self.speed, self.center))
            cur = self.rect
            swept = old.union(cur)
            if self.vx < 0 and left and swept.colliderect(left.rect):
                events.append(self.hit_paddle(left, 1))
            elif self.vx > 0 and right and swept.colliderect(right.rect):
                events.append(self.hit_paddle(right, -1))
            if self.x + self.size < 0:
                return events, 1
            if self.x > WIDTH:
                return events, 0
        return events, None
