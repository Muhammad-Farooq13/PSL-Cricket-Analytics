# Makefile for PSL Data Science Project

.PHONY: help install test lint format clean train serve docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean temporary files"
	@echo "  make train         - Run training pipeline"
	@echo "  make serve         - Start Flask server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	pylint src/

format:
	black src/ tests/ *.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

train:
	python mlops_pipeline.py

serve:
	python flask_app.py

docker-build:
	docker build -t psl-project:latest .

docker-run:
	docker run -p 5000:5000 -v $(PWD)/models:/app/models psl-project:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down
