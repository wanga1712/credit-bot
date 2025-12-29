#!/usr/bin/env python3
"""Тест подключения к разным HTTPS сайтам."""

import requests
import httpx

sites = [
    "https://www.google.com",
    "https://github.com",
    "https://api.telegram.org",
    "https://core.telegram.org",
]

print("Тест подключения к разным сайтам через requests:")
for site in sites:
    try:
        response = requests.get(site, timeout=10)
        print(f"   ✅ {site}: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {site}: {type(e).__name__}")

print("\nТест подключения к разным сайтам через httpx:")
for site in sites:
    try:
        response = httpx.get(site, timeout=10.0)
        print(f"   ✅ {site}: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {site}: {type(e).__name__}")

