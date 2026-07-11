from __future__ import annotations

import pygame

from volley.entities.particles import ParticlePool


def test_particle_pool_burst_caps_to_pool_and_updates() -> None:
    pool = ParticlePool(max_particles=3)
    pool.burst((10, 20), (255, 80, 40), count=10, speed=200)
    active = [particle for particle in pool.particles if particle.active]
    assert len(active) == 3
    before = [(particle.x, particle.y) for particle in active]
    pool.update(0.05)
    after = [(particle.x, particle.y) for particle in active]
    assert after != before
    pool.update(1.0)
    assert not any(particle.active for particle in pool.particles)


def test_particle_draw_handles_active_particles() -> None:
    pygame.init()
    surface = pygame.Surface((64, 64))
    pool = ParticlePool(max_particles=1)
    pool.burst((20, 20), (255, 255, 255), count=1, speed=0)
    pool.draw(surface, offset=(1, 1))
    assert surface.get_at((21, 21))[:3] != (0, 0, 0)
