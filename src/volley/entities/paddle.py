from __future__ import annotations

from dataclasses import dataclass

import pygame

from volley.config import HEIGHT, PADDLE_H, PADDLE_W


@dataclass
class Paddle:
    x: float
    y: float
    speed: float
    width: int = PADDLE_W
    height: int = PADDLE_H

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def move(self, direction: float, dt: float) -> None:
        if direction:
            self.y += direction * self.speed * dt
            self.clamp()

    def track(self, target_y: float, dt: float, dead_zone: float = 8.0) -> None:
        delta = target_y - self.center_y
        if abs(delta) <= dead_zone:
            return
        self.move(1.0 if delta > 0 else -1.0, dt)

    def clamp(self) -> None:
        self.y = max(0.0, min(float(HEIGHT - self.height), self.y))

    def reset(self, y: float | None = None) -> None:
        self.y = y if y is not None else (HEIGHT - self.height) / 2
        self.clamp()
