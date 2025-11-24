.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test coverage lint format clean install-dev

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Confectionery Catalog - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Docker commands
build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

up: ## Start all services
	@echo "$(BLUE)Starting services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started! Application available at http://localhost$(NC)"

down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down

restart: ## Restart all services
	@echo "$(YELLOW)Restarting services...$(NC)"
	docker-compose restart

logs: ## Show logs (use TAIL=100 to limit)
	docker-compose logs -f --tail=${TAIL:-50}

logs-web: ## Show web service logs
	docker-compose logs -f web

logs-db: ## Show database logs
	docker-compose logs -f db

logs-redis: ## Show Redis logs
	docker-compose logs -f redis

# Django commands
shell: ## Open Django shell
	docker-compose exec web python backend/manage.py shell

shell-plus: ## Open Django shell_plus (requires django-extensions)
	docker-compose exec web python backend/manage.py shell_plus

dbshell: ## Open database shell
	docker-compose exec web python backend/manage.py dbshell

bash: ## Open bash in web container
	docker-compose exec web bash

# Database commands
migrate: ## Run database migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	docker-compose exec web python backend/manage.py migrate

makemigrations: ## Create new migrations
	@echo "$(BLUE)Creating migrations...$(NC)"
	docker-compose exec web python backend/manage.py makemigrations

showmigrations: ## Show migration status
	docker-compose exec web python backend/manage.py showmigrations

# User management
createsuperuser: ## Create superuser
	docker-compose exec web python backend/manage.py createsuperuser

# Static files
collectstatic: ## Collect static files
	@echo "$(BLUE)Collecting static files...$(NC)"
	docker-compose exec web python backend/manage.py collectstatic --noinput

# Testing removed from project

# Code quality
lint: ## Run linting (flake8, black check, isort check)
	@echo "$(BLUE)Running linters...$(NC)"
	docker-compose exec web flake8 backend
	docker-compose exec web black --check backend
	docker-compose exec web isort --check-only backend

format: ## Format code (black, isort)
	@echo "$(BLUE)Formatting code...$(NC)"
	docker-compose exec web black backend
	docker-compose exec web isort backend

type-check: ## Run type checking with mypy
	docker-compose exec web mypy backend

# Development setup
init: build up migrate createsuperuser ## Initial setup (build, up, migrate, superuser)
	@echo "$(GREEN)Project initialized successfully!$(NC)"

setup: ## Quick setup for first time (copy env, build, up)
	@if [ ! -f .env ]; then cp .env.example .env; echo "$(GREEN).env file created$(NC)"; fi
	$(MAKE) build
	$(MAKE) up
	@echo "$(GREEN)Setup complete! Migrations are running automatically. Create superuser with 'make createsuperuser'$(NC)"

# Database backup and restore
backup-db: ## Backup database
	@echo "$(BLUE)Backing up database...$(NC)"
	docker-compose exec -T db pg_dump -U postgres confectionery > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Database backed up!$(NC)"

restore-db: ## Restore database (use FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then echo "$(RED)Please specify FILE=backup.sql$(NC)"; exit 1; fi
	@echo "$(YELLOW)Restoring database from $(FILE)...$(NC)"
	docker-compose exec -T db psql -U postgres confectionery < $(FILE)
	@echo "$(GREEN)Database restored!$(NC)"

# Cleanup
clean: ## Remove containers, volumes, and cached files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-all: clean ## Remove all Docker resources including images
	docker-compose down --rmi all -v
	@echo "$(GREEN)All resources removed!$(NC)"

# Redis commands
redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

flush-cache: ## Flush Redis cache
	docker-compose exec redis redis-cli FLUSHALL
	@echo "$(GREEN)Cache flushed!$(NC)"

# Monitoring
ps: ## Show running containers
	docker-compose ps

top: ## Show container resource usage
	docker-compose top

stats: ## Show live container stats
	docker stats

# Production commands
deploy-prod: ## Deploy to production (builds production image)
	@echo "$(BLUE)Building production image...$(NC)"
	docker build -t confectionery-catalog:latest -f Dockerfile .
	@echo "$(GREEN)Production image built!$(NC)"

# Load sample data
loaddata: ## Load sample data fixtures
	docker-compose exec web python backend/manage.py loaddata backend/application/catalog/fixtures/sample_data.json

# Check system
check: ## Run Django system checks
	docker-compose exec web python backend/manage.py check

# API documentation
generate-api-docs: ## Generate OpenAPI schema
	docker-compose exec web python backend/manage.py spectacular --color --file schema.yml
	@echo "$(GREEN)API schema generated in schema.yml$(NC)"

# Quick development workflow
dev: up logs ## Start development (up + follow logs)

reset-db: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all database data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d db; \
		sleep 5; \
		$(MAKE) migrate; \
		echo "$(GREEN)Database reset complete!$(NC)"; \
	fi

# Install development dependencies locally (for IDE support)
install-dev: ## Install dev dependencies locally
	pip install -r requirements/development.txt
	@echo "$(GREEN)Development dependencies installed locally$(NC)"
