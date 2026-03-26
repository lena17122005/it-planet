# Трамплин

Каркас карьерной платформы для взаимодействия студентов, выпускников, работодателей и карьерных центров.

## Что уже сделано на этапе 1
- Подготовлена полная структура `frontend/` и `backend/` согласно ТЗ.
- Настроены базовые конфиги Vite + React + TypeScript + Tailwind + Framer Motion + Leaflet.
- Настроен FastAPI-проект, SQLAlchemy 2.0, JWT-утилиты, CORS.
- Добавлен Alembic + первая миграция с PostgreSQL/PostGIS расширением.
- Добавлены Dockerfile для frontend (production через nginx) и backend.
- Добавлен `docker-compose.yml` на 3 сервиса: `postgres`, `backend`, `frontend`.

## Быстрый старт
1. Скопируйте переменные окружения:
   ```bash
   cp .env.example .env
   ```
2. Запустите приложение:
   ```bash
   docker-compose up --build
   ```
3. Доступ:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

## Следующие этапы
1. Полная реализация ролей и JWT refresh-flow.
2. Модели/схемы/роуты для откликов, контактов, модерации, тегов и приватности.
3. Геокодирование (Nominatim), карта с маркерами разных типов, модальные карточки.
4. Верификация компаний и модерация контента.
5. E2E тестирование пользовательских сценариев.
