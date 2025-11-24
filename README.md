# OptimizedStock API

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF 3.14](https://img.shields.io/badge/DRF-3.14-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

> **Enterprise-grade система управления каталогом и инвентарем**

Production-ready RESTful API с Domain-Driven Design архитектурой. 

**Ключевые технологии**: N+1 query optimization, multi-level caching (Redis), strategic DB indexing, automated CI/CD, comprehensive monitoring.

## 📋 Содержание

- [Технологический Стек](#-технологический-стек)
- [Быстрый Старт](#-быстрый-старт)
- [Архитектура](#-архитектура)
- [API Endpoints](#-api-endpoints)
- [Разработка](#-разработка)

## 🛠 Технологический Стек

**Backend:**
- Python 3.11 • Django 4.2 LTS • Django REST Framework 3.14
- PostgreSQL 15 (JSONB, full-text search, advanced indexing)
- Redis 7 (caching, session management)

**Infrastructure:**
- Docker & Docker Compose (multi-stage builds)
- Nginx (reverse proxy, load balancing)
- Gunicorn (WSGI server)

**Code Quality:**
- Black • Flake8 • isort • mypy
- Pre-commit hooks • Type hints • Comprehensive testing

## 🏗 Архитектура

**Domain-Driven Design** с четким разделением слоев:
- **Domain Layer**: Бизнес-логика и базовые модели
- **Application Layer**: Use cases, API endpoints, сериализация
- **Infrastructure Layer**: Конфигурация, внешние сервисы

**Технические решения:**
- N+1 query optimization (`select_related`, `prefetch_related`, `only/defer`)
- Multi-level caching (Redis TTL strategies, cache warming/invalidation)
- Strategic indexing (composite, partial, GIN/GiST indexes)
- PostgreSQL full-text search (триграммы, ranking)
- OpenAPI 3.0 documentation (drf-spectacular)
- Comprehensive monitoring (health checks, logging, metrics)

## 📁 Структура Проекта

```
OptimizedStock/
├── backend/
│   ├── application/        # Application Layer (Use Cases)
│   │   └── catalog/       # Product catalog module
│   │       ├── api/       # REST API (serializers, views, filters)
│   │       └── models.py  # Domain models
│   ├── domain/            # Domain Layer (Business Logic)
│   │   └── core/         # Core utilities, base models
│   └── infrastructure/    # Infrastructure Layer
│       └── config/       # Settings (base, dev, prod)
├── docker/
├── requirements/
├── docker-compose.yml
├── Dockerfile
└── Makefile
```

## 🚀 Быстрый Старт

**Требования:** Docker 20.10+, Docker Compose 2.0+

```bash
# Клонирование
git clone https://github.com/d1g-1t/OptimizedStock.git
cd OptimizedStock

# Запуск (автоматическая настройка: build, up, migrate)
make setup

# Создание суперпользователя
make createsuperuser
```

**Доступ:**
- API: http://localhost:8002/api/
- Admin: http://localhost:8002/admin/
- Swagger: http://localhost:8002/api/docs/
- Health: http://localhost:8002/health/


## � API Endpoints

**Продукты:**
```
GET    /api/products/              # Список с фильтрацией и поиском
GET    /api/products/{slug}/       # Детали продукта
POST   /api/products/              # Создание (admin)
PUT    /api/products/{slug}/       # Обновление (admin)
DELETE /api/products/{slug}/       # Удаление (admin)
```

**Категории, Топпинги, Обертки:**
```
GET    /api/categories/
GET    /api/toppings/
GET    /api/wrappers/
```

**Возможности:**
- Фильтрация по категории, цене, весу, доступности
- Полнотекстовый поиск по названию и описанию
- Сортировка по множественным полям
- Пагинация (cursor-based/offset)

## � Разработка

**Основные команды:**
```bash
make setup          # Полная настройка
make shell          # Django shell
make migrate        # Применить миграции
make lint           # Линтинг (flake8, black, isort)
make format         # Автоформатирование
make type-check     # Проверка типов (mypy)
make test           # Запуск тестов
```

**Production:**
```bash
docker build -f Dockerfile -t optimizedstock:latest .
```

## 📄 Лицензия

MIT License

---

## 👨‍💻 Технические компетенции

**Backend Architecture:**
- Domain-Driven Design (layered architecture)
- SOLID principles, Design Patterns
- REST API design best practices

**Django Expertise:**
- Advanced ORM (query optimization, custom managers, signals)
- DRF (serializers, viewsets, permissions, filters)
- Middleware, custom management commands

**Database:**
- Query optimization (N+1 prevention, indexing strategies)
- PostgreSQL advanced features (JSONB, full-text search, GIN/GiST)
- Database design, migrations, connection pooling

**Performance:**
- Multi-level caching strategies (Redis)
- Cache invalidation patterns
- Async tasks, background processing

**DevOps:**
- Docker (multi-stage builds, optimization)
- CI/CD pipelines (GitHub Actions)
- Infrastructure as Code
- Monitoring & observability

**Code Quality:**
- Type safety (mypy, type hints)
- Automated testing (unit, integration, API)
- Linting, formatting (black, flake8, isort)
- Pre-commit hooks
