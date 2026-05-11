.PHONY: train estimate setup clean

VENV_BIN := .venv/bin
PYTHON := $(VENV_BIN)/python

# Check if virtual environment exists, if not create it and install dependencies
setup:
	@ if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		$(PYTHON) -m pip install --upgrade pip; \
		$(PYTHON) -m pip install -r src/requirements.txt; \
	fi
	@echo "Virtual environment is set up and dependencies are installed."

train:
	$(PYTHON) src/Train/Train.py

estimate:
	$(PYTHON) src/Estimate/Estimate.py

run: train

plot:
	$(PYTHON) src/Plot/Plot.py data/data.csv

clean:
	@echo "Cleaning project artifacts..."
	@if [ -d ".venv" ]; then rm -rf .venv; else echo "No .venv to remove"; fi
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@find . -type f -name "*.pyc" -delete || true
	@rm -rf build/ dist/ *.egg-info .pytest_cache || true
	@rm -f Plot/*.png || true
