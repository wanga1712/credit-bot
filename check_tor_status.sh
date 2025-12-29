#!/bin/bash
# Скрипт проверки статуса Tor

echo "=========================================="
echo "Проверка статуса Tor"
echo "=========================================="

# Проверка статуса службы
echo ""
echo "1. Статус службы Tor:"
sudo systemctl status tor --no-pager -l | head -20

# Проверка порта
echo ""
echo "2. Проверка порта 9050:"
sudo ss -tlnp | grep 9050

# Проверка логов
echo ""
echo "3. Последние логи Tor:"
sudo journalctl -u tor -n 30 --no-pager

# Проверка подключения через Tor
echo ""
echo "4. Проверка подключения через Tor:"
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip 2>/dev/null | head -5

echo ""
echo "=========================================="

