#!/bin/bash
cd ~/credit_bot
# Останавливаем все старые процессы
pkill -9 -f 'python.*main.py' 2>/dev/null
sleep 2
# Запускаем бота
source venv/bin/activate
nohup python main.py > bot.log 2>&1 &
sleep 3
# Проверяем статус
ps aux | grep '[p]ython main.py'
echo "---"
tail -10 bot.log
