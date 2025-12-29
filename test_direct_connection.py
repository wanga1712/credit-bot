#!/usr/bin/env python3
"""Проверка прямого подключения к Telegram API без прокси."""

import asyncio
import httpx
import socket

async def test_direct_connection():
    """Проверяет прямое подключение к Telegram API."""
    print("Проверка прямого подключения к Telegram API (без прокси)...\n")
    
    # 1. Проверка DNS
    print("1. Проверка DNS для api.telegram.org...")
    try:
        ip = socket.gethostbyname("api.telegram.org")
        print(f"   ✅ DNS разрешен: {ip}")
    except socket.gaierror as e:
        print(f"   ❌ Ошибка DNS: {e}")
        return False
    
    # 2. Проверка TCP подключения
    print("\n2. Проверка TCP подключения к api.telegram.org:443...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex(("api.telegram.org", 443))
        sock.close()
        if result == 0:
            print(f"   ✅ TCP подключение успешно")
        else:
            print(f"   ❌ TCP подключение не удалось (код: {result})")
            print(f"   💡 Telegram API заблокирован или недоступен")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка TCP подключения: {e}")
        return False
    
    # 3. Проверка HTTPS подключения
    print("\n3. Проверка HTTPS подключения...")
    try:
        timeout = httpx.Timeout(10.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get("https://api.telegram.org", timeout=timeout)
            print(f"   ✅ HTTPS подключение успешно (статус: {response.status_code})")
            return True
    except httpx.ConnectTimeout:
        print(f"   ❌ Таймаут подключения")
        print(f"   💡 Telegram API заблокирован или недоступен")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка HTTPS: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_direct_connection())
    if result:
        print("\n✅ Прямое подключение работает! Можно отключить прокси.")
    else:
        print("\n❌ Прямое подключение не работает. Нужен прокси или VPN.")

