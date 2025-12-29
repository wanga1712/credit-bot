#!/usr/bin/env python3
"""Скрипт для проверки подключения к Telegram API."""

import sys
import asyncio
import httpx
from pathlib import Path
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

TELEGRAM_API = "https://api.telegram.org"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


async def check_connection():
    """Проверяет подключение к Telegram API."""
    
    print("=" * 60)
    print("Проверка подключения к Telegram API")
    print("=" * 60)
    
    # Проверка 1: Базовое подключение к API
    print("\n1. Проверка базового подключения к api.telegram.org...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TELEGRAM_API}/")
            print(f"   ✅ Подключение успешно! Статус: {response.status_code}")
    except httpx.ConnectTimeout:
        print("   ❌ Таймаут подключения - сервер не может подключиться к api.telegram.org")
        print("   💡 Возможные причины:")
        print("      - Telegram API заблокирован в вашей сети")
        print("      - Проблемы с файрволом")
        print("      - Проблемы с DNS")
        return False
    except httpx.ConnectError as e:
        print(f"   ❌ Ошибка подключения: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Неожиданная ошибка: {e}")
        return False
    
    # Проверка 2: Проверка токена (если указан)
    if BOT_TOKEN:
        print(f"\n2. Проверка токена бота...")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{TELEGRAM_API}/bot{BOT_TOKEN}/getMe"
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        bot_info = data.get("result", {})
                        print(f"   ✅ Токен валиден!")
                        print(f"   bot_id: {bot_info.get('id')}")
                        print(f"   username: @{bot_info.get('username')}")
                        print(f"   first_name: {bot_info.get('first_name')}")
                    else:
                        print(f"   ❌ Токен невалиден: {data.get('description')}")
                        return False
                else:
                    print(f"   ❌ Ошибка API: {response.status_code}")
                    print(f"   Ответ: {response.text}")
                    return False
        except httpx.ConnectTimeout:
            print("   ❌ Таймаут при проверке токена")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка при проверке токена: {e}")
            return False
    else:
        print("\n2. Токен не указан в .env (пропуск проверки токена)")
    
    # Проверка 3: Проверка прокси (если указан)
    proxy_url = os.getenv("TELEGRAM_PROXY")
    if proxy_url:
        print(f"\n3. Проверка прокси: {proxy_url}")
        try:
            async with httpx.AsyncClient(
                timeout=10.0,
                proxies=proxy_url
            ) as client:
                response = await client.get(f"{TELEGRAM_API}/")
                print(f"   ✅ Прокси работает! Статус: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Прокси не работает: {e}")
            return False
    else:
        print("\n3. Прокси не настроен")
    
    print("\n" + "=" * 60)
    print("✅ Все проверки пройдены успешно!")
    print("=" * 60)
    return True


async def check_dns():
    """Проверяет разрешение DNS для api.telegram.org."""
    import socket
    
    print("\nПроверка DNS для api.telegram.org...")
    try:
        ip = socket.gethostbyname("api.telegram.org")
        print(f"   ✅ DNS разрешен: {ip}")
        return True
    except socket.gaierror as e:
        print(f"   ❌ Ошибка DNS: {e}")
        return False


if __name__ == "__main__":
    print("\n🔍 Диагностика подключения к Telegram API\n")
    
    # Проверка DNS
    asyncio.run(check_dns())
    
    # Основная проверка
    success = asyncio.run(check_connection())
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ ПРОБЛЕМЫ С ПОДКЛЮЧЕНИЕМ")
        print("=" * 60)
        print("\nРекомендации:")
        print("1. Проверьте доступность api.telegram.org:")
        print("   curl -I https://api.telegram.org")
        print("\n2. Если Telegram заблокирован, настройте прокси в .env:")
        print("   TELEGRAM_PROXY=http://your-proxy:port")
        print("\n3. Проверьте файрвол:")
        print("   sudo ufw status")
        print("\n4. Подробнее см. NETWORK_TROUBLESHOOTING.md")
        sys.exit(1)
    else:
        print("\n✅ Сервер может подключиться к Telegram API!")
        print("   Если бот все еще не работает, проблема в коде, а не в сети.")
        sys.exit(0)

