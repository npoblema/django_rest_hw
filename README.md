# Online Education REST API

Проект системы дистанционного обучения на Django REST Framework с автоматизированным деплоем через GitHub Actions.

## Технологический стек
- Python 3.10
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Gunicorn
- Nginx
- Docker

## Настройка удаленного сервера

### 1. Подготовка сервера
```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка базовых компонентов
sudo apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis-server

# Установка Docker
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
```
2. Настройка безопасности
```bash
# Настройка фаервола
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable

# Настройка SSH
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```
3. Настройка Systemd для Gunicorn

Создайте файл /etc/systemd/system/gunicorn.service:

ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/online-education-rest-api
ExecStart=/home/ubuntu/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
4. Настройка Nginx
Создайте файл /etc/nginx/sites-available/online-education:

nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/online-education-rest-api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
GitHub Actions Workflow
Создайте файл .github/workflows/deploy.yml:

yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Copy files via SSH
      uses: appleboy/scp-action@master
      with:
        host: ${{ secrets.SERVER_IP }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        source: "./"
        target: "/home/ubuntu/online-education-rest-api"
    - name: Restart services
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_IP }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /home/ubuntu/online-education-rest-api
          docker-compose down
          docker-compose up -d --build
Настройка переменных окружения
Создайте файл .env.example в репозитории:

ini
DEBUG=0
SECRET_KEY=your_secret_key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=online_education
DB_USER=online_education_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
Добавьте в Secrets GitHub:

SERVER_IP - IP адрес сервера

SERVER_USER - пользователь сервера

SSH_PRIVATE_KEY - приватный SSH ключ

Все переменные из .env.example

Инструкция по деплою
Создайте ветку для изменений:

```bash
git checkout -b feature/deployment
```
Добавьте файлы и сделайте коммит:

```bash
git add .github/workflows/deploy.yml .env.example README.md
git commit -m "Add CI/CD pipeline configuration"
```
Создайте Pull Request в ветку develop:

```bash
git push origin feature/deployment
```
После успешного прохождения тестов и ревью кода, изменения можно мержить в main для автоматического деплоя.

Проверка работоспособности
Проверьте статус workflow в GitHub Actions

Убедитесь, что приложение доступно по IP сервера

Проверьте логи:

```bash
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
docker-compose logs -f
```
Критерии выполнения
Сервер настроен с необходимыми пакетами

Приложение доступно по IP/домену

Настроена безопасность сервера

Реализован автоматический перезапуск через Systemd

GitHub Actions workflow включает тесты и деплой

Все секреты вынесены в переменные окружения

Pull request создан в ветку develop

README содержит полные инструкции
