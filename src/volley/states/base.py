from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol

import pygame

from volley.config import StateId


class GameContext(Protocol):
    screen: pygame.Surface
    surface: pygame.Surface
    fonts: dict[str, pygame.font.Font]
    running: bool

    def change_state(self, state_id: StateId) -> None: ...


class GameState(ABC):
    state_id: StateId

    def __init__(self, ctx: Any) -> None:
        self.ctx = ctx

    def enter(self) -> None:
        return None

    def exit(self) -> None:
        return None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
