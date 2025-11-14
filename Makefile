# FastAPI Interview Application - Makefile

.PHONY: help build up down logs shell test clean

# Default target
help:
	@echo "FastAPI Interview Application Commands:"
	@echo "  make build     - Build the Docker image"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View application logs"
	@echo "  make shell     - Access application shell"
	@echo "  make db-shell  - Access PostgreSQL shell"
	@echo "  make mongo     - Access MongoDB shell"
	@echo "  make test      - Run tests (if available)"
	@echo "  make clean     - Clean up containers and images"
	@echo "  make restart   - Restart the application"

# Build the Docker image
build:
	@echo "🔨 Building FastAPI application..."
	docker-compose build

# Start all services
up:
	@echo "🚀 Starting all services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "📊 API Documentation: http://localhost:8000/docs"

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker-compose down

# View logs
logs:
	docker-compose logs -f app

# Access application shell
shell:
	docker-compose exec app /bin/bash

# Access PostgreSQL shell
db-shell:
	docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Access MongoDB shell
mongo:
	docker-compose exec mongodb mongosh -u fastapi_user -p fastapi_password

# Run tests (placeholder)
test:
	@echo "🧪 Running tests..."
	docker-compose exec app python -m pytest

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

# Restart services
restart: down up

# Show service status
status:
	docker-compose ps

# View service logs
logs-all:
	docker-compose logs

# Update and restart
update: build restart

# Database migration
migrate:
	@echo "🔄 Running database migrations..."
	docker-compose exec app alembic upgrade head