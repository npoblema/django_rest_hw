# Online Education REST API

Проект системы дистанционного обучения, построенный на Django, DRF, PostgreSQL, Redis и Celery.

## Развертывание с помощью Docker Compose

### Необходимые компоненты
- Установленный Docker
- Docker Compose версии 1.29+

### Инструкция по запуску

1. Клонирование репозитория:
```bash
git clone https://github.com/
```

Настройка переменных окружения:

```bash
cp .env.example .env && nano .env
```
Сборка и запуск контейнеров:
```bash
docker-compose up -d --build
```
Проверка работы компонентов:
Бэкенд (Django):

```bash
curl http://localhost:8000/api/healthcheck/
```
Тестирование PostgreSQL:
```bash
docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1"
```
Проверка Redis:
```bash
docker-compose exec redis redis-cli ping
```
Мониторинг Celery:
```bash
docker-compose logs -f celery-worker
```
Проверка Celery Beat:
```bash
docker-compose logs -f celery-beat
```
Остановка системы
Штатная остановка:
```bash
docker-compose down
```
Полная очистка (с удалением данных):
```bash
docker-compose down -v --remove-orphans
```
Рекомендации по разработке
Настройка .gitignore:
```bash
cat > .gitignore <<EOL
```
# Environment
.env
.env.local

# IDE
.idea/
.vscode/

# Virtual environment
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo

# Database
db.sqlite3
*.db

# Media
media/
uploads/
EOL
Работа с Git:

```bash
git checkout -b feature/docker-deploy
git add .
git commit -m "Add docker-compose configuration"
git push origin feature/docker-deploy
```
Верификация перед деплоем
Проверка зависимостей сервисов:

```bash
docker-compose config
```
Тестирование доступности API:

```bash
curl -I http://localhost:8000/admin/
```
Проверка логов:

```bash
docker-compose logs --tail=50
```
Для дополнительной информации или проблем с развертыванием создайте issue в репозитории проекта.
