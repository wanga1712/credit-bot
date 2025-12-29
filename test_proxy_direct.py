#!/usr/bin/env python3
"""Проверка прямого подключения к прокси."""

import asyncio
import httpx
import socket
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Получаем прокси из .env, если указан
proxy_url = os.getenv("TELEGRAM_PROXY", "")
if proxy_url:
    # Парсим URL прокси
    if proxy_url.startswith("socks5://"):
        # SOCKS5 прокси (например, Tor)
        proxy_host_port = proxy_url.replace("socks5://", "").split(":")
        PROXY_HOST = proxy_host_port[0]
        PROXY_PORT = int(proxy_host_port[1]) if len(proxy_host_port) > 1 else 9050
        PROXY_TYPE = "socks5"
    elif proxy_url.startswith("http://"):
        # HTTP прокси
        proxy_host_port = proxy_url.replace("http://", "").split(":")
        PROXY_HOST = proxy_host_port[0]
        PROXY_PORT = int(proxy_host_port[1]) if len(proxy_host_port) > 1 else 8080
        PROXY_TYPE = "http"
    else:
        # По умолчанию HTTP
        proxy_host_port = proxy_url.split(":")
        PROXY_HOST = proxy_host_port[0]
        PROXY_PORT = int(proxy_host_port[1]) if len(proxy_host_port) > 1 else 8080
        PROXY_TYPE = "http"
    print(f"📋 Используется прокси из .env: {proxy_url}")
else:
    # Значения по умолчанию (для обратной совместимости)
    PROXY_HOST = "124.122.2.12"
    PROXY_PORT = 8080
    PROXY_TYPE = "http"
    print("⚠️  Прокси не указан в .env, используются значения по умолчанию")

async def test_proxy_connection():
    """Проверяет подключение к прокси."""
    print(f"\nПроверка подключения к прокси {PROXY_HOST}:{PROXY_PORT} (тип: {PROXY_TYPE})...")
    
    # 1. Проверка TCP подключения
    print("\n1. Проверка TCP подключения к прокси...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((PROXY_HOST, PROXY_PORT))
        sock.close()
        if result == 0:
            print(f"   ✅ TCP подключение успешно")
        else:
            print(f"   ❌ TCP подключение не удалось (код: {result})")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка TCP подключения: {e}")
        return False
    
    # 2. Проверка через httpx
    print("\n2. Проверка через httpx...")
    try:
        timeout = httpx.Timeout(10.0, connect=10.0)
        proxy_str = f"{PROXY_TYPE}://{PROXY_HOST}:{PROXY_PORT}"
        async with httpx.AsyncClient(
            timeout=timeout,
            proxies=proxy_str
        ) as client:
            # Пробуем подключиться к простому HTTP-сайту через прокси
            response = await client.get("http://httpbin.org/ip", timeout=timeout)
            print(f"   ✅ httpx подключение успешно (статус: {response.status_code})")
            return True
    except httpx.ConnectTimeout:
        print(f"   ❌ Таймаут подключения через httpx")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка httpx: {type(e).__name__}: {e}")
        return False
    
    # 3. Проверка HTTPS туннелирования
    print("\n3. Проверка HTTPS туннелирования через прокси...")
    try:
        timeout = httpx.Timeout(10.0, connect=10.0)
        proxy_str = f"{PROXY_TYPE}://{PROXY_HOST}:{PROXY_PORT}"
        async with httpx.AsyncClient(
            timeout=timeout,
            proxies=proxy_str
        ) as client:
            response = await client.get("https://api.telegram.org", timeout=timeout)
            print(f"   ✅ HTTPS туннелирование работает (статус: {response.status_code})")
            return True
    except httpx.ConnectTimeout:
        print(f"   ❌ Таймаут при HTTPS туннелировании")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка HTTPS туннелирования: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_proxy_connection())
