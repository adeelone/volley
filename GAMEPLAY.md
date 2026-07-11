# Gameplay

## Modes

- `1 Player vs AI`: left paddle against a right-side AI.
- `2 Player`: local W/S vs Up/Down.
- `Rally Survival`: one paddle, score the longest rally before missing.

## Rules

Standard matches end when one side reaches the configured target score and leads by at least two. The default target is 11.

## Controls

| Action | Default |
| --- | --- |
| P1 up/down | W / S |
| P2 up/down | Up / Down |
| Pause/back | Esc |
| Debug overlay | F3 |
| Fullscreen | F11 |
| Menu navigation | Arrow keys, W/S, Enter/Space, mouse |

## AI Tiers

- Rookie waits until the ball crosses midfield, reacts late, moves slower, and has bounded targeting error.
- Pro tracks from serve, predicts wall bounces, and moves at human paddle speed.
- Legendary has zero modeled reaction delay, moves faster, and varies target position for sharper returns.
