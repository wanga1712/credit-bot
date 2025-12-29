#!/usr/bin/env python3
"""Простой тест подключения разными способами."""

import sys

print("Тест 1: requests (если установлен)")
try:
    import requests
    response = requests.get('https://api.telegram.org', timeout=10)
    print(f"   ✅ requests работает! Статус: {response.status_code}")
except ImportError:
    print("   ⚠️  requests не установлен")
except Exception as e:
    print(f"   ❌ requests ошибка: {e}")

print("\nТест 2: httpx (текущая версия)")
try:
    import httpx
    print(f"   Версия httpx: {httpx.__version__}")
    response = httpx.get('https://api.telegram.org', timeout=10.0)
    print(f"   ✅ httpx работает! Статус: {response.status_code}")
except Exception as e:
    print(f"   ❌ httpx ошибка: {type(e).__name__}: {e}")

print("\nТест 3: httpx с явным IPv4")
try:
    import httpx
    # Принудительно используем IPv4
    import socket
    import httpx._config
    
    # Создаем клиент с явными настройками
    client = httpx.Client(
        timeout=httpx.Timeout(30.0, connect=30.0),
        verify=True,
        follow_redirects=True
    )
    response = client.get('https://api.telegram.org', timeout=30.0)
    print(f"   ✅ httpx с IPv4 работает! Статус: {response.status_code}")
    client.close()
except Exception as e:
    print(f"   ❌ httpx с IPv4 ошибка: {type(e).__name__}: {e}")

print("\nТест 4: Проверка SSL сертификатов")
try:
    import ssl
    import socket
    
    context = ssl.create_default_context()
    with socket.create_connection(('api.telegram.org', 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname='api.telegram.org') as ssock:
            print(f"   ✅ SSL соединение работает!")
            print(f"   Сертификат: {ssock.getpeercert()['subject']}")
except Exception as e:
    print(f"   ❌ SSL ошибка: {type(e).__name__}: {e}")

print("\nТест 5: Проверка DNS резолвинга")
try:
    import socket
    ip = socket.gethostbyname('api.telegram.org')
    print(f"   ✅ DNS работает! IP: {ip}")
except Exception as e:
    print(f"   ❌ DNS ошибка: {type(e).__name__}: {e}")

