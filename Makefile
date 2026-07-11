.PHONY: install run test lint format typecheck build sfx clean

PYTHON ?= python

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) -m volley.main

test:
	SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy $(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests scripts

format:
	$(PYTHON) -m black src tests scripts

typecheck:
	$(PYTHON) -m mypy src tests scripts

build:
	$(PYTHON) -m PyInstaller --noconfirm --name Volley --windowed --collect-data volley src/volley/main.py

sfx:
	$(PYTHON) scripts/generate_sfx.py

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['build','dist','.pytest_cache','.mypy_cache','.ruff_cache']]; [p.unlink() for p in pathlib.Path('.').glob('*.spec')]"
