.PHONY: train estimate setup

VENV_BIN := .venv/bin
PYTHON := $(VENV_BIN)/python

setup:
	@echo "Virtual environment already exists at .venv"
	@$(PYTHON) --version

train:
	$(PYTHON) src/Train/Train.py

estimate:
	$(PYTHON) src/Estimate/Estimate.py

run: train

.DEFAULT_GOAL := train
