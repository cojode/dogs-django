# Dogs and breeds

## Установка

### 1. Клонирование репозитория

```sh
git clone https://github.com/cojode/dogs-django.git
```

Скопируйте и настройте .env файл:

```sh
cp .env.exanple .env
```

### 2. Запуск внутри контейнера

Убедитесь что находитесь в корне проекта:

```sh
docker compose up --build
```

### Ресурсы

По умолчанию проект запускается на ```localhost:8000```

Swagger документация: ```localhost:8000/swagger```

Redoc документация: ```localhost:8000/redoc```

## Эндопоинты
```
GET (список) на /api/dogs/
POST на /api/dogs/
GET на /api/dogs/<id>
PUT на /api/dogs/<id>
DELETE на /api/dogs/<id>

GET (список) на /api/breeds/
POST на /api/breeds/
GET на /api/breeds/<id>
PUT на /api/breeds/<id>
DELETE на /api/breeds/<id>
```
Подробнее в ресурсах документации

## Тестирование

Тесты для ```dogs_api``` хранятся в ```dogs/dogs_api/tests.py```

### Запуск тестов

Локально:

```sh
cd cafe_manager
python manage.py test
```

В контейнере:

```sh
docker compose up test --build
```

## Структура проекта
Проект следует классической архитектуре Django
```sh
├── docker-compose.yml
├── Dockerfile
├── dogs
│   ├── dogs
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── dogs_api
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models
│   │   ├── serializers.py - сериализаторы моделей
│   │   ├── tests.py - тесты приложения
│   │   ├── urls.py - роутер приложения
│   │   └── views.py - эндпоинты приложения(ModelViewSet)
│   └── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
└── requirements.txt
```
