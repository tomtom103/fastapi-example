VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
HOST = 0.0.0.0
PORT = 5000
DIR=./app

SHELL := /bin/bash
.ONESHELL:

.PHONY: help dev run test clean

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To run the project type make run, all dependencies will be installed"
	@echo "To run the project in a dev environment type make dev, uses ngrok to communicate"
	@echo "To clean the project type make clean"
	@echo "------------------------------------"

dev: $(VENV)/bin/activate
	USE_NGROK=true $(PYTHON) $(DIR)/debug.py 

run: $(VENV)/bin/activate
	uvicorn app.main:app --host $(HOST) --port $(PORT)

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) freeze > requirements.txt

test:
	$(PYTHON) -m pytest

clean:
	rm -rf **/__pycache__
	rm -rf .pytest_cache
