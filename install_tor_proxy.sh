#!/bin/bash
# Скрипт установки Tor для использования только ботом

set -e

echo "=========================================="
echo "Установка Tor для прокси бота"
echo "=========================================="

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Этот скрипт требует прав root. Запустите с sudo:"
    echo "   sudo bash install_tor_proxy.sh"
    exit 1
fi

# Определение дистрибутива
if [ -f /etc/debian_version ]; then
    DISTRO="debian"
elif [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
else
    echo "❌ Неподдерживаемый дистрибутив. Установите Tor вручную."
    exit 1
fi

if [ "$DISTRO" = "debian" ]; then
    echo "📦 Установка Tor для Debian/Ubuntu..."
    
    # Обновление пакетов
    apt update
    
    # Установка Tor
    apt install -y tor
    
    echo "✅ Tor установлен!"
    
elif [ "$DISTRO" = "rhel" ]; then
    echo "📦 Установка Tor для RHEL/CentOS..."
    
    # Установка EPEL репозитория (если еще не установлен)
    if ! rpm -q epel-release > /dev/null 2>&1; then
        yum install -y epel-release
    fi
    
    # Установка Tor
    yum install -y tor
    
    echo "✅ Tor установлен!"
fi

# Настройка Tor для работы как SOCKS5 прокси
echo ""
echo "🔧 Настройка Tor..."

# Создание резервной копии конфига
if [ -f /etc/tor/torrc ]; then
    cp /etc/tor/torrc /etc/tor/torrc.backup.$(date +%Y%m%d_%H%M%S)
fi

# Проверка, не настроен ли уже Tor
if ! grep -q "^SOCKSPort 127.0.0.1:9050" /etc/tor/torrc; then
    # Добавление настройки SOCKS порта (если еще нет)
    if ! grep -q "^SOCKSPort" /etc/tor/torrc; then
        echo "" >> /etc/tor/torrc
        echo "# SOCKS5 прокси для бота (только локальный доступ)" >> /etc/tor/torrc
        echo "SOCKSPort 127.0.0.1:9050" >> /etc/tor/torrc
    fi
fi

# Запуск и включение автозапуска
systemctl enable tor
systemctl restart tor

# Проверка статуса
sleep 2
if systemctl is-active --quiet tor; then
    echo "✅ Tor запущен и работает!"
    echo ""
    echo "📝 Следующие шаги:"
    echo "   1. Добавьте в .env файл:"
    echo "      TELEGRAM_PROXY=socks5://127.0.0.1:9050"
    echo ""
    echo "   2. Проверьте подключение:"
    echo "      python test_proxy_direct.py"
    echo ""
    echo "   3. Запустите бота:"
    echo "      python main.py"
    echo ""
    echo "💡 Tor будет работать только для бота через .env"
    echo "   Остальные соединения сервера не будут использовать Tor"
    echo ""
else
    echo "❌ Ошибка запуска Tor. Проверьте логи:"
    echo "   sudo journalctl -u tor -n 50"
    exit 1
fi

