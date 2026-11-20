#!/bin/sh
set -e

mkdir -p logs certs

if [ ! -f certs/jwt-private.pem ]; then
    echo "Generating JWT keys..."
    openssl genrsa -out certs/jwt-private.pem 2048
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
fi

alembic upgrade head

# Тестовые данные из seed.sql — только если база пустая (первый запуск)
python seed.py

exec uvicorn main:main_app --host 0.0.0.0 --port 8000 --reload
