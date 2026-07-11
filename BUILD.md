# Build

Install development dependencies first:

```bash
python -m pip install -e ".[dev]"
python scripts/generate_sfx.py
```

Build for the current OS:

```bash
python -m PyInstaller --noconfirm --name Volley --windowed --collect-data volley src/volley/main.py
```

Output appears under `dist/Volley/`. PyInstaller builds are OS-specific, so build Windows binaries on Windows, macOS binaries on macOS, and Linux binaries on Linux.

Pygame packaging gotchas:

- Include package data with `--collect-data volley`.
- Regenerate audio assets before building.
- Use a clean virtual environment if a build includes unexpected packages.
