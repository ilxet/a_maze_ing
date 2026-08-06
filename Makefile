ifeq ($(OS),Windows_NT)
	VENV := .venv
	PYTHON := $(VENV)/Scripts/python.exe
	PIP := $(VENV)/Scripts/pip.exe
else
	VENV := .venv
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
endif

CONFIG := config.txt

.PHONY: help venv install run debug lint lint-strict clean

help:
	@echo "Available targets:"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run maze generator"
	@echo "  make debug        - Run with pdb"
	@echo "  make lint         - Run flake8 and mypy"
	@echo "  make lint-strict  - Run strict mypy"
	@echo "  make clean        - Remove caches"

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy .

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

clean:
	$(PYTHON) -c "import pathlib, shutil; \
	for p in pathlib.Path('.').rglob('__pycache__'): shutil.rmtree(p, ignore_errors=True); \
	for p in pathlib.Path('.').rglob('.mypy_cache'): shutil.rmtree(p, ignore_errors=True); \
	for p in pathlib.Path('.').rglob('.pytest_cache'): shutil.rmtree(p, ignore_errors=True); \
	shutil.rmtree('build', ignore_errors=True); \
	shutil.rmtree('dist', ignore_errors=True); \
	[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('*.egg-info')]"