# Инструкция по настройке Git репозитория

## Шаг 1: Создание удаленного репозитория

### Вариант A: GitHub (рекомендуется)

1. Перейдите на [GitHub.com](https://github.com) и войдите в аккаунт
2. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните форму:
   - **Repository name**: `credit-bot` (или любое другое имя)
   - **Description**: "Telegram-бот для расчёта кредитов"
   - **Visibility**: выберите **Private** (если не хотите публичный) или **Public**
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license" (у нас уже есть эти файлы)
4. Нажмите **"Create repository"**

### Вариант B: GitLab

1. Перейдите на [GitLab.com](https://gitlab.com) и войдите в аккаунт
2. Нажмите **"New project"** → **"Create blank project"**
3. Заполните форму:
   - **Project name**: `credit-bot`
   - **Visibility Level**: выберите нужный уровень доступа
4. Нажмите **"Create project"**

### Вариант C: Bitbucket

1. Перейдите на [Bitbucket.org](https://bitbucket.org) и войдите в аккаунт
2. Нажмите **"Create"** → **"Repository"**
3. Заполните форму и создайте репозиторий

## Шаг 2: Отправка кода в удаленный репозиторий

После создания репозитория на GitHub/GitLab/Bitbucket, выполните следующие команды **на вашем Windows компьютере**:

```bash
# Перейдите в директорию проекта
cd C:\Users\wangr\PycharmProjects\pythonProject93

# Создайте первый коммит (если еще не создан)
git commit -m "Initial commit: Credit Bot project"

# Добавьте удаленный репозиторий
# ЗАМЕНИТЕ <username> и <repository-name> на ваши значения
git remote add origin https://github.com/<username>/<repository-name>.git

# Или если используете SSH:
# git remote add origin git@github.com:<username>/<repository-name>.git

# Отправьте код в удаленный репозиторий
git push -u origin master
```

**Пример для GitHub:**
```bash
git remote add origin https://github.com/yourusername/credit-bot.git
git push -u origin master
```

**Если у вас уже есть коммиты и вы хотите переименовать ветку в main:**
```bash
git branch -M main
git push -u origin main
```

## Шаг 3: Клонирование на Linux сервере

После того, как код отправлен в удаленный репозиторий, на **Linux сервере** выполните:

### Вариант 1: HTTPS (проще, требует ввода логина/пароля)

```bash
# Клонируйте репозиторий
git clone https://github.com/<username>/<repository-name>.git

# Перейдите в директорию проекта
cd <repository-name>
```

**Пример:**
```bash
git clone https://github.com/yourusername/credit-bot.git
cd credit-bot
```

### Вариант 2: SSH (удобнее, не требует ввода пароля каждый раз)

**Сначала настройте SSH ключ на Linux сервере:**

```bash
# Генерируйте SSH ключ (если еще нет)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Покажите публичный ключ
cat ~/.ssh/id_ed25519.pub
```

Скопируйте вывод и добавьте его в настройки GitHub/GitLab:
- **GitHub**: Settings → SSH and GPG keys → New SSH key
- **GitLab**: Preferences → SSH Keys

**Затем клонируйте:**

```bash
# Клонируйте репозиторий через SSH
git clone git@github.com:<username>/<repository-name>.git

# Перейдите в директорию проекта
cd <repository-name>
```

**Пример:**
```bash
git clone git@github.com:yourusername/credit-bot.git
cd credit-bot
```

## Шаг 4: Настройка на Linux сервере

После клонирования выполните:

```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте виртуальное окружение
source venv/bin/activate

# Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Создайте файл .env
nano .env
# Добавьте строку: TELEGRAM_BOT_TOKEN=ваш_токен_здесь
# Сохраните: Ctrl+O, Enter, Ctrl+X

# Запустите бота
python main.py
```

## Полезные команды Git

### Проверка статуса
```bash
git status
```

### Просмотр удаленных репозиториев
```bash
git remote -v
```

### Обновление кода на сервере
```bash
cd /path/to/project
git pull origin master  # или main
```

### Просмотр истории коммитов
```bash
git log --oneline
```

## Решение проблем

### Ошибка: "remote origin already exists"
```bash
# Удалите существующий remote
git remote remove origin
# Добавьте заново
git remote add origin <url>
```

### Ошибка: "Permission denied (publickey)"
- Убедитесь, что SSH ключ добавлен в GitHub/GitLab
- Проверьте: `ssh -T git@github.com`

### Ошибка: "fatal: refusing to merge unrelated histories"
```bash
git pull origin master --allow-unrelated-histories
```

