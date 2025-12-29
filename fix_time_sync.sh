#!/bin/bash
# Исправление времени на сервере

echo "=== Исправление времени на сервере ==="

echo "1. Текущее время на сервере:"
date

echo ""
echo "2. Установка и настройка NTP..."
sudo apt update
sudo apt install -y ntp ntpdate

echo ""
echo "3. Синхронизация времени с NTP серверами..."
sudo ntpdate -s time.nist.gov || sudo ntpdate -s pool.ntp.org

echo ""
echo "4. Настройка автоматической синхронизации..."
# Останавливаем старый ntp если запущен
sudo systemctl stop ntp 2>/dev/null || true

# Синхронизируем время
sudo ntpdate -s pool.ntp.org || sudo ntpdate -s time.nist.gov

# Запускаем systemd-timesyncd (если доступен)
sudo systemctl enable systemd-timesyncd 2>/dev/null || true
sudo systemctl start systemd-timesyncd 2>/dev/null || true

# Или используем ntp
sudo systemctl enable ntp 2>/dev/null || true
sudo systemctl start ntp 2>/dev/null || true

echo ""
echo "5. Новое время на сервере:"
date

echo ""
echo "6. Проверка синхронизации:"
timedatectl status 2>/dev/null || echo "timedatectl недоступен, используйте: date"

echo ""
echo "=== Готово! ==="
echo "Попробуйте теперь:"
echo "python check_telegram_connection.py"

