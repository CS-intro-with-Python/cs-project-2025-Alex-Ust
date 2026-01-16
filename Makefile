.PHONY: help install run client test test-unit test-integration docker-up docker-down

PYTHON ?= python3
PIP ?= pip3

help:
	@echo "Targets:"
	@echo "  install           Install Python deps"
	@echo "  run               Run server (requires DATABASE_URL)"
	@echo "  client            Run client script"
	@echo "  test              Run unit + integration tests"
	@echo "  test-unit         Run unit tests"
	@echo "  test-integration  Run integration tests (Docker up)"
	@echo "  docker-up         Start Docker Compose"
	@echo "  docker-down       Stop Docker Compose and remove volumes"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) server.py

client:
	$(PYTHON) client.py

test: test-unit test-integration

test-unit:
	pytest -s unit_testing.py

test-integration:
	pytest -s integration_testing.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v
