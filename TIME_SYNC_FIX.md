# Исправление проблемы с временем на сервере

## Проблема
Неправильное время на сервере может вызывать проблемы с SSL/TLS handshake, так как:
- SSL сертификаты имеют временные ограничения (valid from/to)
- Если время на сервере сильно отличается от реального, сертификат может считаться невалидным
- Это приводит к таймаутам SSL handshake

## Решение

### Автоматическое исправление

```bash
cd ~/credit-bot
git pull origin main
chmod +x fix_time_sync.sh
./fix_time_sync.sh
```

### Ручное исправление

**1. Проверьте текущее время:**
```bash
date
```

**2. Установите NTP:**
```bash
sudo apt update
sudo apt install -y ntp ntpdate
```

**3. Синхронизируйте время:**
```bash
sudo ntpdate -s pool.ntp.org
# или
sudo ntpdate -s time.nist.gov
```

**4. Настройте автоматическую синхронизацию:**

Для systemd:
```bash
sudo systemctl enable systemd-timesyncd
sudo systemctl start systemd-timesyncd
sudo timedatectl set-ntp true
```

Для ntp:
```bash
sudo systemctl enable ntp
sudo systemctl start ntp
```

**5. Проверьте время:**
```bash
date
timedatectl status
```

## Проверка после исправления

```bash
# 1. Проверьте время
date

# 2. Проверьте подключение к Telegram
python check_telegram_connection.py

# 3. Если работает, запустите бота
python main.py
```

## Важно

- Время должно быть синхронизировано с точностью до нескольких секунд
- Разница более 5 минут может вызывать проблемы с SSL
- После исправления времени SSL handshake должен работать

