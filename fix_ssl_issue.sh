#!/bin/bash
# Скрипт для исправления проблем с SSL в Python

echo "=== Исправление проблем с SSL в Python ==="

echo "1. Проверка версии OpenSSL в Python..."
python3 -c "import ssl; print(f'OpenSSL версия: {ssl.OPENSSL_VERSION}')"

echo ""
echo "2. Обновление certifi (сертификаты SSL)..."
pip install --upgrade certifi

echo ""
echo "3. Обновление httpx и зависимостей..."
pip install --upgrade httpx httpcore anyio

echo ""
echo "4. Проверка сертификатов..."
python3 -c "import certifi; import ssl; ctx = ssl.create_default_context(cafile=certifi.where()); print(f'Сертификаты найдены: {certifi.where()}')"

echo ""
echo "5. Установка requests для теста..."
pip install requests

echo ""
echo "=== Готово! Попробуйте запустить: python test_connection_simple.py ==="

