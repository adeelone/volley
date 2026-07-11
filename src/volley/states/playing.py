from __future__ import annotations

import random

import pygame

from volley.ai import AiController
from volley.config import HEIGHT, HUMAN_PADDLE_SPEED, RALLY_MAX_SPEED, WIDTH, Mode, StateId
from volley.entities.ball import Ball
from volley.entities.paddle import Paddle
from volley.entities.particles import ParticlePool
from volley.settings import RallyScore, save_high_score
from volley.states.base import GameState
from volley.ui.text_fx import draw_center_text


class PlayingState(GameState):
    state_id = StateId.PLAYING

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.left = Paddle(42, (HEIGHT - 96) / 2, HUMAN_PADDLE_SPEED)
        self.right = Paddle(WIDTH - 58, (HEIGHT - 96) / 2, HUMAN_PADDLE_SPEED)
        self.ball = Ball()
        self.particles = ParticlePool()
        self.score = [0, 0]
        self.rally = 0
        self.max_rally_speed = 0
        self.serve_dir = 1
        self.ai = AiController(self.ctx.difficulty)
        self.shake = 0.0
        self.score_pop = 0.0

    def new_match(self) -> None:
        self.score = [0, 0]
        self.rally = 0
        self.max_rally_speed = 0
        self.left.reset()
        self.right.reset()
        self.ai = AiController(self.ctx.difficulty)
        self.serve_dir = random.choice([-1, 1]) if self.ctx.settings.serve_random else 1
        self.ball.max_speed = RALLY_MAX_SPEED if self.ctx.mode is Mode.RALLY else self.ctx.ball_max_speed
        self.ball.reset(self.serve_dir, self.ctx.settings.serve_random)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ctx.change_state(StateId.PAUSED)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        kb = self.ctx.settings.keys
        self.left.move((1 if keys[kb.p1_down] else 0) - (1 if keys[kb.p1_up] else 0), dt)
        right_active = self.ctx.mode is Mode.TWO_PLAYER
        if right_active:
            self.right.move((1 if keys[kb.p2_down] else 0) - (1 if keys[kb.p2_up] else 0), dt)
        elif self.ctx.mode is Mode.VS_AI:
            self.ai.update(self.ball, self.right, dt)
        else:
            self.right.y = -200
        events, point = self.ball.update(
            dt,
            self.left,
            self.right if self.ctx.mode is not Mode.RALLY else None,
            self.ctx.settings.ball_trail,
        )
        for event in events:
            self.ctx.audio.play("paddle" if event.kind == "paddle" else "wall")
            burst = 6 if self.ctx.settings.reduce_motion else 18
            self.particles.burst(event.pos, self.ctx.theme.accent, burst, event.speed)
            if event.kind == "paddle":
                self.rally += 1
                self.max_rally_speed = max(self.max_rally_speed, round(event.speed))
                if not self.ctx.settings.reduce_motion:
                    self.shake = min(8.0, event.speed / 100)
        self.particles.update(dt)
        self.shake = max(0.0, self.shake - dt * 24)
        self.score_pop = max(0.0, self.score_pop - dt)
        if point is not None:
            self.handle_point(point)

    def handle_point(self, point: int) -> None:
        self.ctx.audio.play("score")
        if self.ctx.mode is Mode.RALLY:
            save_high_score(RallyScore(self.rally, self.max_rally_speed))
            self.ctx.winner = "Rally ended"
            self.ctx.final_score = f"Rally {self.rally} | Max speed {self.max_rally_speed}"
            self.ctx.change_state(StateId.GAME_OVER)
            return
        self.score[point] += 1
        self.score_pop = 0.35
        if self.is_match_over():
            self.ctx.winner = "Left Paddle Wins" if self.score[0] > self.score[1] else "Right Paddle Wins"
            self.ctx.final_score = f"{self.score[0]} - {self.score[1]}"
            self.ctx.change_state(StateId.GAME_OVER)
            return
        self.serve_dir = -1 if point == 0 else 1
        self.ball.reset(self.serve_dir, self.ctx.settings.serve_random)
        self.ctx.change_state(StateId.COUNTDOWN)

    def is_match_over(self) -> bool:
        high = max(self.score)
        low = min(self.score)
        return high >= self.ctx.settings.win_score and high - low >= 2

    def draw(self, screen: pygame.Surface) -> None:
        theme = self.ctx.theme
        screen.fill(theme.background)
        for y in range(12, HEIGHT, 34):
            pygame.draw.rect(screen, theme.muted, pygame.Rect(WIDTH // 2 - 2, y, 4, 18))
        ox = oy = 0
        if self.shake > 0 and not self.ctx.settings.reduce_motion:
            ox = random.randint(-round(self.shake), round(self.shake))
            oy = random.randint(-round(self.shake), round(self.shake))
        if self.ctx.settings.ball_trail:
            for trail_x, trail_y, age in self.ball.trail:
                alpha = max(20, round(180 * age / 0.3))
                color = tuple(c * alpha // 255 for c in theme.ball)
                rect = pygame.Rect(round(trail_x + ox), round(trail_y + oy), self.ball.size, self.ball.size)
                pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, theme.paddle, self.left.rect.move(ox, oy), border_radius=3)
        if self.ctx.mode is not Mode.RALLY:
            pygame.draw.rect(screen, theme.paddle, self.right.rect.move(ox, oy), border_radius=3)
        pygame.draw.rect(screen, theme.ball, self.ball.rect.move(ox, oy), border_radius=4)
        self.particles.draw(screen, (ox, oy))
        score_text = f"{self.score[0]}   {self.score[1]}" if self.ctx.mode is not Mode.RALLY else f"Rally {self.rally}"
        font = self.ctx.fonts["score"]
        if self.score_pop > 0:
            font = self.ctx.fonts["title"]
        draw_center_text(screen, font, score_text, theme.text, (480, 54))
        if self.ctx.debug:
            debug_text = f"FPS {self.ctx.clock.get_fps():.0f} | ball {self.ball.speed:.0f}"
            draw_center_text(screen, self.ctx.fonts["small"], debug_text, theme.accent, (830, 22))
