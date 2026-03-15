# CI/CD Django Project

## Описание проекта

Проект представляет собой Django/DRF приложение, которое разворачивается с помощью Docker Compose.
Для автоматизации тестирования и деплоя используется GitHub Actions.

Pipeline выполняет:

* запуск тестов Django
* сборку Docker образов
* деплой приложения на удалённый сервер

---

# CI/CD Pipeline

Workflow расположен в директории:

.github/workflows/ci.yml

Pipeline запускается:

* при каждом **push в репозиторий**
* при создании **Pull Request в ветку develop**

## Этапы pipeline

### 1. Test stage

На этом этапе:

* происходит checkout репозитория
* устанавливается Python
* устанавливаются зависимости проекта
* запускаются тесты Django

Команда запуска тестов:

```bash
python manage.py test
```

Если тесты завершаются с ошибкой, следующие этапы pipeline не выполняются.

---

### 2. Deploy stage

Если тесты прошли успешно, запускается деплой приложения.

Во время деплоя:

* создаётся файл `.env` из GitHub Secrets
* выполняется сборка Docker образов
* перезапускаются контейнеры приложения

---

# Настройка удалённого сервера

1. Подключитесь к серверу по SSH:

```bash
ssh login@SERVER_IP
```

2. Установите Docker и Docker Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

3. Добавьте пользователя в группу docker:

```bash
sudo usermod -aG docker $USER
```

После этого перезапустите SSH-сессию.

4. Проверьте работу Docker:

```bash
docker ps
```

---

# Настройка GitHub Actions Runner

1. Перейдите в репозиторий GitHub.

Settings → Actions → Runners

2. Нажмите **New self-hosted runner**.

3. На сервере выполните команды установки runner:

```bash
mkdir actions-runner
cd actions-runner

curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.314.1/actions-runner-linux-x64-2.314.1.tar.gz

tar xzf ./actions-runner-linux-x64.tar.gz
```

4. Настройте runner:

```bash
./config.sh --url https://github.com/USERNAME/REPOSITORY --token TOKEN
```

5. Запустите runner:

```bash
./run.sh
```

После этого runner появится в GitHub и будет выполнять workflow.

---

# Настройка переменных окружения

В GitHub необходимо создать секрет:

DOTENV

В него помещается содержимое файла `.env`.

Пример `.env.example`:

```env
DJANGO_SECRET_KEY=secret_key
DEBUG=False

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

REDIS_HOST=redis
REDIS_PORT=6379
```

Файл `.env` не должен коммититься в репозиторий.

---

# Запуск проекта с помощью Docker Compose

## Предварительные требования

На системе должны быть установлены:

* Docker
* Docker Compose

В проекте должны присутствовать файлы:

* Dockerfile
* docker-compose.yaml
* .env.example

---

## Настройка переменных окружения

Скопируйте `.env.example`:

```bash
cp .env.example .env
```

После этого отредактируйте переменные:

* DJANGO_SECRET_KEY
* POSTGRES_PASSWORD
* другие переменные при необходимости.

---

## Запуск проекта

Собрать образы и запустить контейнеры:

```bash
docker-compose -f docker-compose.yml up -d --build
```

или

```bash
docker-compose up -d --build
```

---

# Сервисы проекта

После запуска будут работать следующие контейнеры:

* backend — Django/DRF API
* db — база данных PostgreSQL
* redis — брокер сообщений Redis
* celery — Celery worker
* celery-beat — планировщик задач Celery Beat

---

# Проверка работы сервисов

## Backend

Откройте в браузере:

http://localhost:8000

---

## PostgreSQL

Проверьте статус контейнеров:

```bash
docker-compose ps
```

Контейнер `db` должен иметь статус **healthy**.

---

## Redis

Проверка Redis из контейнера backend:

```bash
docker-compose exec backend python -c "import redis; r = redis.Redis(host='redis', port=6379); print(r.ping())"
```

---

## Celery Worker

Просмотр логов:

```bash
docker-compose logs -f celery
```

---

## Celery Beat

Просмотр логов:

```bash
docker-compose logs -f celery-beat
```

---

# Остановка контейнеров

Остановить сервисы:

```bash
docker-compose down
```

Остановить и удалить volume базы данных:

```bash
docker-compose down -v
```

---

# Деплой приложения

После push в репозиторий GitHub Actions запускает pipeline.

Если тесты проходят успешно, выполняется деплой:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
```

Контейнеры пересобираются, и приложение обновляется на сервере.

---
