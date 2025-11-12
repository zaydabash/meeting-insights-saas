.PHONY: help setup dev test lint format migrate seed clean

help:
	@echo "Available targets:"
	@echo "  make setup    - Initial setup (install deps, create .env)"
	@echo "  make dev      - Start all services in dev mode"
	@echo "  make test     - Run all tests"
	@echo "  make lint     - Run linters"
	@echo "  make format   - Format code"
	@echo "  make migrate  - Run database migrations"
	@echo "  make seed     - Seed database with demo data"
	@echo "  make clean    - Clean temporary files"

setup:
	@echo "Setting up project..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi
	@cd apps/api && python -m venv venv || true
	@cd apps/api && . venv/bin/activate && pip install -r requirements.txt
	@cd apps/admin && npm install
	@echo "Setup complete. Edit .env with your configuration."

dev:
	@echo "Starting development environment..."
	docker-compose -f infra/docker-compose.yml up --build

test:
	@echo "Running tests..."
	@cd apps/api && . venv/bin/activate && pytest
	@cd apps/admin && npm test

lint:
	@echo "Running linters..."
	@cd apps/api && . venv/bin/activate && ruff check . && mypy .
	@cd apps/admin && npm run lint

format:
	@echo "Formatting code..."
	@cd apps/api && . venv/bin/activate && ruff format . && black .
	@cd apps/admin && npm run format

migrate:
	@echo "Running migrations..."
	@cd apps/api && . venv/bin/activate && alembic upgrade head

migrate-create:
	@echo "Creating migration..."
	@cd apps/api && . venv/bin/activate && alembic revision --autogenerate -m "$(msg)"

seed:
	@echo "Seeding database..."
	@cd apps/api && . venv/bin/activate && python scripts/seed.py

clean:
	@echo "Cleaning..."
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true

