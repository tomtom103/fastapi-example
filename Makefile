PYTHON := python3.10

.venv:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install --upgrade pip-tools

requirements.txt: pyproject.toml | .venv
	.venv/bin/pip-compile \
		--resolver=backtracking \
		--no-emit-trusted-host \
		--no-emit-index-url \
		--generate-hashes \
		--upgrade \
		--output-file $@ \
		pyproject.toml

requirements-dev.txt: pyproject.toml requirements.txt | .venv
	.venv/bin/pip-compile \
		--resolver=backtracking \
		--no-emit-trusted-host \
		--no-emit-index-url \
		--generate-hashes \
		--all-extras \
		--upgrade \
		--output-file $@ \
		requirements.txt \
		pyproject.toml

.venv/sentinel: requirements-dev.txt | .venv
	.venv/bin/pip-sync \
		--pip-args '--no-deps' \
		requirements-dev.txt
	.venv/bin/pip install --no-deps --editable .
	touch $@


.PHONY: dev
dev: .venv/sentinel

.PHONY: build
build: | .venv
	.venv/bin/pip install build
	.venv/bin/python -m build .

.PHONY: lint
lint: | dev
	.venv/bin/mypy

.PHONY: format
format: | dev
	.venv/bin/python -m black src tests
	.venv/bin/ruff check --fix
