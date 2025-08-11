SHELL := /bin/bash

PYPI_TOKEN := ${PYPI_TOKEN}

.PHONY: lint
lint:
	@uv run ruff format ./src
	@uv run ruff check ./src --fix
	@uv run mypy ./src

.PHONY: clean
clean:
	@rm -rf dist

.PHONY: build
build: lint clean
	@echo "Cleaning dist/"
	@uv build

publish-test:
	@twine upload --repository-url https://test.pypi.org/legacy/ -u __token__ -p $(PYPI_TOKEN) dist/* 

publish: build
	@twine upload -u __token__ -p $(PYPI_TOKEN) dist/*
