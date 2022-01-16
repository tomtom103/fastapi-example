VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
HOST = 0.0.0.0
PORT = 5000
DIR=./app

SHELL := /bin/bash
.ONESHELL:

.PHONY: help run test clean

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To run the project type make run, all dependencies will be installed"
	@echo "To clean the project type make clean"
	@echo "------------------------------------"

run: $(VENV)/bin/activate
	$(PYTHON) $(DIR)/main.py

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) freeze > requirements.txt

test:
	$(PYTHON) -m pytest

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	rm -rf .pytest_cache
