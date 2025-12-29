#!/bin/bash
# Скрипт удаления Tor

set -e

echo "=========================================="
echo "Удаление Tor"
echo "=========================================="

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Этот скрипт требует прав root. Запустите с sudo:"
    echo "   sudo bash remove_tor.sh"
    exit 1
fi

# Остановка Tor
echo "🛑 Остановка Tor..."
systemctl stop tor 2>/dev/null || true
systemctl disable tor 2>/dev/null || true

# Удаление Tor
echo "🗑️  Удаление Tor..."
if command -v apt &> /dev/null; then
    apt remove -y tor
    apt autoremove -y
elif command -v yum &> /dev/null; then
    yum remove -y tor
fi

echo "✅ Tor удален!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Найдите HTTP-прокси на https://www.proxy-list.download/"
echo "   2. Обновите .env файл:"
echo "      nano ~/credit-bot/.env"
echo "      TELEGRAM_PROXY=http://новый-ip:порт"
echo "   3. Запустите бота:"
echo "      cd ~/credit-bot && python main.py"
echo ""

