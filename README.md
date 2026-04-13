# Django Classifier API

REST API для управления иерархическим классификатором товаров.

## Запуск

```bash
git clone https://github.com/Alexandra-1203/django-classifier-api.git
cd django-classifier-api
cp .env.example .env
docker compose up --build
```

API будет доступно по адресу: http://localhost:8000/api/categories/

API Эндпоинты

```markdown
Категории
GET /api/categories/ Список всех категорий (плоский)
POST /api/categories/ Создать категорию
GET /api/categories/{id}/ Получить категорию по ID
PUT /api/categories/{id}/ Полное обновление категории
PATCH /api/categories/{id}/ Частичное обновление категории
DELETE /api/categories/{id}/ Удалить категорию (дочерние переподвешиваются к родителю)
GET /api/categories/{id}/descendants/ Все потомки категории (с уровнями вложенности)
GET /api/categories/{id}/parents/ Все предки категории
PUT /api/categories/{id}/change_parent/ Переместить категорию к новому родителю (с проверкой на циклы)
GET /api/categories/{id}/terminals/ Все листовые категории в поддереве
GET /api/categories/{id}/products/ Все продукты в этой категории

Продукты
GET /api/products/ Список всех продуктов
POST /api/products/ Создать продукт (с привязкой к категории)
GET /api/products/{id}/ Получить продукт по ID
PUT /api/products/{id}/ Полное обновление продукта
PATCH /api/products/{id}/ Частичное обновление продукта
DELETE /api/products/{id}/ Удалить продукт
GET /api/products/{id}/parents/ Получить всех предков продукта (категории)
```

Стек:

```markdown
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.0-green)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/DRF-3.15-red)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/docker-compose-blue)](https://www.docker.com/)
```
