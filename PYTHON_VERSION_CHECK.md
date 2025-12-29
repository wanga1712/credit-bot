# Проверка и установка Python на Linux

## Проверка текущей версии Python

Выполните на сервере:

```bash
# Проверьте версию Python 3
python3 --version

# Или
python3 -V

# Проверьте, установлен ли Python вообще
which python3
```

## Требования проекта

Проект требует **Python 3.11 или выше** (включая 3.13).

## Если Python не установлен или версия ниже 3.11

### Ubuntu/Debian:

```bash
# Обновите список пакетов
sudo apt update

# Установите Python 3.11 (или 3.12, или 3.13)
sudo apt install python3.11 python3.11-venv python3.11-pip

# Или для Python 3.13 (если доступен в репозиториях)
sudo apt install python3.13 python3.13-venv python3.13-pip
```

### Если нужна именно версия 3.13 (через deadsnakes PPA для Ubuntu):

```bash
# Добавьте репозиторий
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Установите Python 3.13
sudo apt install python3.13 python3.13-venv python3.13-pip
```

### CentOS/RHEL:

```bash
# Установите Python 3.11 из EPEL
sudo yum install epel-release
sudo yum install python311 python311-pip
```

## Создание виртуального окружения с правильной версией

**ВАЖНО:** Виртуальное окружение нужно создавать **внутри директории проекта**, а не в домашней директории!

```bash
# Перейдите в директорию проекта
cd ~/credit-bot

# Создайте виртуальное окружение с конкретной версией Python
python3.11 -m venv venv
# или
python3.13 -m venv venv

# Активируйте виртуальное окружение
source venv/bin/activate

# Проверьте версию Python в виртуальном окружении
python --version

# Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt
```

## Проверка совместимости

После активации виртуального окружения проверьте:

```bash
python --version  # Должно быть 3.11 или выше
pip --version     # Должна быть установлена pip
```

