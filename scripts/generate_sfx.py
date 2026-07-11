from __future__ import annotations

import math
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "volley" / "assets"
RATE = 44100


def write_wave(path: Path, freqs: list[float], seconds: float, volume: float = 0.35) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = bytearray()
    total = int(RATE * seconds)
    for i in range(total):
        t = i / RATE
        env = max(0.0, 1.0 - i / total)
        sample = sum(math.sin(math.tau * f * t) for f in freqs) / len(freqs)
        val = int(max(-1, min(1, sample * env * volume)) * 32767)
        frames.extend(val.to_bytes(2, "little", signed=True))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(frames)


def main() -> None:
    specs = {
        "paddle": ([220, 440], 0.08),
        "wall": ([180, 260], 0.06),
        "score": ([392, 523, 659], 0.24),
        "tick": ([660], 0.08),
        "menu": ([330, 495], 0.05),
        "confirm": ([392, 588, 784], 0.14),
        "win": ([523, 659, 784, 1046], 0.42),
        "lose": ([220, 196, 174], 0.36),
    }
    for name, (freqs, seconds) in specs.items():
        write_wave(ROOT / "sfx" / f"{name}.wav", list(freqs), seconds)
    write_wave(ROOT / "music" / "loop.wav", [110, 165, 220, 330], 3.5, volume=0.16)


if __name__ == "__main__":
    main()
