from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    background: tuple[int, int, int]
    panel: tuple[int, int, int]
    text: tuple[int, int, int]
    muted: tuple[int, int, int]
    accent: tuple[int, int, int]
    accent2: tuple[int, int, int]
    paddle: tuple[int, int, int]
    ball: tuple[int, int, int]


THEMES: dict[str, Theme] = {
    "Classic mono": Theme(
        "Classic mono", (9, 11, 12), (22, 24, 26), (238, 238, 232), (136, 140, 142),
        (238, 238, 232), (80, 84, 86), (238, 238, 232), (238, 238, 232)
    ),
    "Neon": Theme(
        "Neon", (5, 7, 18), (18, 22, 45), (238, 247, 255), (127, 147, 184),
        (45, 232, 210), (255, 80, 170), (45, 232, 210), (255, 236, 96)
    ),
    "Sunset": Theme(
        "Sunset", (24, 18, 30), (46, 35, 55), (255, 243, 224), (187, 151, 141),
        (255, 132, 94), (84, 196, 204), (255, 196, 118), (255, 245, 190)
    ),
}


def get_theme(name: str) -> Theme:
    return THEMES.get(name, THEMES["Classic mono"])
