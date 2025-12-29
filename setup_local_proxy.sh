#!/bin/bash
# Установка локального прокси на сервере

echo "=== Установка локального прокси ==="

# Вариант 1: tinyproxy (простой HTTP прокси)
echo "1. Установка tinyproxy..."
sudo apt update
sudo apt install -y tinyproxy

echo "2. Настройка tinyproxy..."
# Создаем бэкап оригинального конфига
sudo cp /etc/tinyproxy/tinyproxy.conf /etc/tinyproxy/tinyproxy.conf.backup

# Настраиваем tinyproxy для работы как локальный прокси
sudo tee /etc/tinyproxy/tinyproxy.conf > /dev/null <<EOF
User tinyproxy
Group tinyproxy
Port 8888
Timeout 600
DefaultErrorFile "/usr/share/tinyproxy/default.html"
StatFile "/usr/share/tinyproxy/stats.html"
Logfile "/var/log/tinyproxy/tinyproxy.log"
LogLevel Info
PidFile "/var/run/tinyproxy/tinyproxy.pid"
MaxClients 100
MinSpareServers 5
MaxSpareServers 20
StartServers 10
MaxRequestsPerChild 0
Allow 127.0.0.1
Allow ::1
ViaProxyName "tinyproxy"
EOF

echo "3. Запуск tinyproxy..."
sudo systemctl enable tinyproxy
sudo systemctl restart tinyproxy
sudo systemctl status tinyproxy --no-pager

echo ""
echo "=== Готово! ==="
echo "Прокси запущен на порту 8888"
echo "Добавьте в .env:"
echo "TELEGRAM_PROXY=http://127.0.0.1:8888"
echo ""
echo "Проверка:"
echo "curl --proxy http://127.0.0.1:8888 https://api.telegram.org"

