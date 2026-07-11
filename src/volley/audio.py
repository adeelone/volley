from __future__ import annotations

import logging
from pathlib import Path

import pygame

LOG = logging.getLogger(__name__)


class AudioManager:
    def __init__(self, asset_root: Path, music_volume: float, sfx_volume: float) -> None:
        self.asset_root = asset_root
        self.music_volume = music_volume
        self.sfx_volume = sfx_volume
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except pygame.error as exc:
            LOG.warning("Audio disabled: %s", exc)
        if self.enabled:
            self._load_sounds()

    def _load_sounds(self) -> None:
        for name in ["paddle", "wall", "score", "tick", "menu", "confirm", "win", "lose"]:
            path = self.asset_root / "sfx" / f"{name}.wav"
            try:
                self.sounds[name] = pygame.mixer.Sound(str(path))
            except pygame.error as exc:
                LOG.warning("Could not load sound %s: %s", path, exc)

    def set_volumes(self, music: float, sfx: float) -> None:
        self.music_volume = max(0.0, min(1.0, music))
        self.sfx_volume = max(0.0, min(1.0, sfx))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume)

    def play(self, name: str) -> None:
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(self.sfx_volume)
            sound.play()

    def start_music(self) -> None:
        if not self.enabled:
            return
        path = self.asset_root / "music" / "loop.wav"
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)
        except pygame.error as exc:
            LOG.warning("Could not start music %s: %s", path, exc)

    def stop_music(self) -> None:
        if self.enabled:
            pygame.mixer.music.stop()
