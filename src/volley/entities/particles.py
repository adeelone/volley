from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame


@dataclass
class Particle:
    x: float = 0
    y: float = 0
    vx: float = 0
    vy: float = 0
    life: float = 0
    color: tuple[int, int, int] = (255, 255, 255)
    radius: float = 2
    active: bool = False


class ParticlePool:
    def __init__(self, max_particles: int = 220) -> None:
        self.particles = [Particle() for _ in range(max_particles)]

    def burst(self, pos: tuple[float, float], color: tuple[int, int, int], count: int, speed: float) -> None:
        for particle in self.particles:
            if count <= 0:
                break
            if particle.active:
                continue
            angle = random.random() * math.tau
            mag = random.uniform(50, 150) + speed * 0.08
            particle.x, particle.y = pos
            particle.vx = math.cos(angle) * mag
            particle.vy = math.sin(angle) * mag
            particle.life = random.uniform(0.18, 0.45)
            particle.radius = random.uniform(1.5, 3.6)
            particle.color = color
            particle.active = True
            count -= 1

    def update(self, dt: float) -> None:
        for particle in self.particles:
            if not particle.active:
                continue
            particle.life -= dt
            if particle.life <= 0:
                particle.active = False
                continue
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            particle.vx *= 0.98
            particle.vy *= 0.98

    def draw(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        ox, oy = offset
        for particle in self.particles:
            if particle.active:
                alpha = max(40, min(255, int(255 * particle.life / 0.45)))
                color = tuple(max(0, min(255, c * alpha // 255)) for c in particle.color)
                pygame.draw.circle(
                    surface,
                    color,
                    (round(particle.x + ox), round(particle.y + oy)),
                    round(particle.radius),
                )
