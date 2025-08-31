#!make
-include .env
export $(shell sed 's/=.*//' .env)
SHELL := /bin/bash

IMAGE_NAME = code.abifog.com/packages/tasks2bookstack:latest

.PHONY: *

build:
	uv pip compile pyproject.toml > requirements.txt
	uvx pex -r requirements.txt . -o ./build/tasks2bookstack -e tasks2bookstack.main:main --python python3
	podman build -t $(IMAGE_NAME) .
	podman push $(IMAGE_NAME)

develop:
	uv venv ./.venv
	uv sync
	uv pip install -e .
	touch .env

format:
	uv tool run ruff format ./src

lint:
	uv tool run ruff check --fix src/
	uv tool run ruff check

mypy:
	mypy ./src

run:
	tasks2bookstack  -c ./drafts/config.yaml

run-container:
	podman run --rm -it \
		--name friday \
		-v $(PWD)/config/example.yml:/app/config.yml:ro,z \
		$(IMAGE_NAME) tasks2bookstack
