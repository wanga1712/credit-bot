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

PROXY_HOST = "124.122.2.12"
PROXY_PORT = 8080

async def test_proxy_connection():
    """Проверяет подключение к прокси."""
    print(f"Проверка подключения к прокси {PROXY_HOST}:{PROXY_PORT}...")
    
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
        async with httpx.AsyncClient(
            timeout=timeout,
            proxies=f"http://{PROXY_HOST}:{PROXY_PORT}"
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
        async with httpx.AsyncClient(
            timeout=timeout,
            proxies=f"http://{PROXY_HOST}:{PROXY_PORT}"
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

