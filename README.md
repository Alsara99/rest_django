## Запуск проекта с помощью Docker Compose

### Предварительные требования

- **Docker** и **Docker Compose** установлены на машине.
- В корне проекта есть:
  - `Dockerfile` для Django/DRF-приложения,
  - `docker-compose.yaml` (этот файл),
  - шаблон переменных окружения `.env.example`

### Настройка переменных окружения

1. Скопируйте шаблон `.env.example` в файл `.env`:

   ```bash
   cp .env.example .env
   ```

2. Откройте `.env` и задайте реальные значения:
   - `DJANGO_SECRET_KEY`
   - `POSTGRES_PASSWORD`
   - при необходимости другие переменные.

Файл `.env` в репозиторий **не коммитится** (он игнорируется через `.gitignore`).

### Запуск проекта

Собрать образы и запустить все сервисы в фоновом режиме:

```bash
docker-compose -f docker-compose.yaml up -d --build
```

Или, если ваша версия Docker Compose автоматически подхватывает `docker-compose.yaml`:

```bash
docker-compose up -d --build
```

Будут запущены сервисы:

- **backend** — Django/DRF API
- **db** — база данных PostgreSQL
- **redis** — брокер сообщений Redis
- **celery** — Celery worker
- **celery-beat** — планировщик задач Celery Beat

### Проверка работоспособности сервисов

- **Backend (Django/DRF)**  
  Откройте в браузере:

  ```text
  http://localhost:8000/
  ```

  (или порт, указанный в `BACKEND_PORT` в `.env`).

- **PostgreSQL (db)**  
  Проверьте статус контейнера и хелсчек:

  ```bash
  docker-compose ps
  ```

  Статус сервиса `db` должен быть `healthy`.

- **Redis**  
  Проверьте, что контейнер работает:

  ```bash
  docker-compose ps
  ```

  Дополнительно можно обратиться к Redis из контейнера `backend`:

  ```bash
  docker-compose exec backend python -c "import redis; r = redis.Redis(host='redis', port=6379); print(r.ping())"
  ```

- **Celery worker**  
  Посмотреть логи воркера:

  ```bash
  docker-compose logs -f celery
  ```

- **Celery Beat**  
  Посмотреть логи планировщика:

  ```bash
  docker-compose logs -f celery-beat
  ```

### Остановка и очистка

Остановить все контейнеры и удалить контейнеры и сети:

```bash
docker-compose down
```

Остановить и дополнительно удалить том с данными PostgreSQL:

```bash
docker-compose down -v
```

# Homework_34-2
