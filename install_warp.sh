#!/bin/bash
# Скрипт установки Cloudflare WARP

set -e

echo "=========================================="
echo "Установка Cloudflare WARP"
echo "=========================================="

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Этот скрипт требует прав root. Запустите с sudo:"
    echo "   sudo bash install_warp.sh"
    exit 1
fi

# Определение дистрибутива
if [ -f /etc/debian_version ]; then
    DISTRO="debian"
elif [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
else
    echo "❌ Неподдерживаемый дистрибутив. Установите WARP вручную."
    exit 1
fi

if [ "$DISTRO" = "debian" ]; then
    echo "📦 Установка для Debian/Ubuntu..."
    
    # Добавление репозитория
    curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/cloudflare-client.list
    
    # Обновление и установка
    apt update
    apt install -y cloudflare-warp
    
    echo "✅ WARP установлен!"
    echo ""
    echo "📝 Следующие шаги:"
    echo "   1. Зарегистрируйтесь: warp-cli register"
    echo "   2. Подключитесь: warp-cli connect"
    echo "   3. Проверьте статус: warp-cli status"
    echo "   4. Удалите TELEGRAM_PROXY из .env файла"
    echo ""
    
elif [ "$DISTRO" = "rhel" ]; then
    echo "📦 Установка для RHEL/CentOS..."
    
    # Добавление репозитория
    rpm -ivh https://pkg.cloudflareclient.com/cloudflare-release-el8.rpm
    
    # Установка
    yum install -y cloudflare-warp
    
    echo "✅ WARP установлен!"
    echo ""
    echo "📝 Следующие шаги:"
    echo "   1. Зарегистрируйтесь: warp-cli register"
    echo "   2. Подключитесь: warp-cli connect"
    echo "   3. Проверьте статус: warp-cli status"
    echo "   4. Удалите TELEGRAM_PROXY из .env файла"
    echo ""
fi

