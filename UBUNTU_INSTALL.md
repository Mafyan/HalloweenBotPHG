# 🐧 Инструкция по установке бота на Ubuntu 20.04

## 📋 Требования

- Ubuntu 20.04 или выше
- Root доступ или sudo права
- Интернет соединение

## 🚀 Установка

### Шаг 1: Обновление системы

```bash
sudo apt update
sudo apt upgrade -y
```

### Шаг 2: Установка Python 3 и pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

Проверьте версию Python (должна быть 3.8+):
```bash
python3 --version
```

### Шаг 3: Установка Git

```bash
sudo apt install git -y
```

### Шаг 4: Клонирование репозитория

```bash
cd /opt
sudo git clone https://github.com/Mafyan/HalloweenBotPHG.git
cd HalloweenBotPHG
```

Или клонируйте в домашнюю директорию:
```bash
cd ~
git clone https://github.com/Mafyan/HalloweenBotPHG.git
cd HalloweenBotPHG
```

### Шаг 5: Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 6: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 7: Проверка конфигурации

Откройте файл `config.py` и убедитесь, что все данные корректны:

```bash
nano config.py
```

Проверьте:
- `BOT_TOKEN` - токен вашего бота
- `MODERATION_CHAT_ID` - ID модераторского чата
- `DEADLINE` - дата и время дедлайна

Сохраните: `Ctrl + O`, `Enter`, выход: `Ctrl + X`

## 🔧 Запуск бота

### Запуск в терминале (для тестирования)

```bash
source venv/bin/activate
python3 bot.py
```

Для остановки: `Ctrl + C`

### Запуск в фоновом режиме с помощью screen

Установите screen:
```bash
sudo apt install screen -y
```

Создайте новую сессию:
```bash
screen -S halloween_bot
```

Запустите бота:
```bash
cd ~/HalloweenBotPHG  # или /opt/HalloweenBotPHG
source venv/bin/activate
python3 bot.py
```

Отключитесь от сессии: `Ctrl + A`, затем `D`

Вернуться к боту:
```bash
screen -r halloween_bot
```

Список всех сессий:
```bash
screen -ls
```

### Запуск в фоновом режиме с помощью tmux

Установите tmux:
```bash
sudo apt install tmux -y
```

Создайте новую сессию:
```bash
tmux new -s halloween_bot
```

Запустите бота:
```bash
cd ~/HalloweenBotPHG  # или /opt/HalloweenBotPHG
source venv/bin/activate
python3 bot.py
```

Отключитесь от сессии: `Ctrl + B`, затем `D`

Вернуться к боту:
```bash
tmux attach -t halloween_bot
```

## 🔄 Автозапуск с помощью systemd (рекомендуется)

### Создайте systemd сервис

```bash
sudo nano /etc/systemd/system/halloween-bot.service
```

Вставьте следующее содержимое (измените пути если нужно):

```ini
[Unit]
Description=Halloween Contest Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/HalloweenBotPHG
Environment="PATH=/home/your_username/HalloweenBotPHG/venv/bin"
ExecStart=/home/your_username/HalloweenBotPHG/venv/bin/python3 /home/your_username/HalloweenBotPHG/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**ВАЖНО:** Замените `your_username` на ваше имя пользователя! Узнать его можно командой: `whoami`

Если установили в `/opt`, используйте:
```ini
User=root
WorkingDirectory=/opt/HalloweenBotPHG
Environment="PATH=/opt/HalloweenBotPHG/venv/bin"
ExecStart=/opt/HalloweenBotPHG/venv/bin/python3 /opt/HalloweenBotPHG/bot.py
```

### Включите и запустите сервис

```bash
# Перезагрузите конфигурацию systemd
sudo systemctl daemon-reload

# Включите автозапуск при старте системы
sudo systemctl enable halloween-bot

# Запустите бота
sudo systemctl start halloween-bot

# Проверьте статус
sudo systemctl status halloween-bot
```

### Полезные команды для управления сервисом

```bash
# Остановить бота
sudo systemctl stop halloween-bot

# Перезапустить бота
sudo systemctl restart halloween-bot

# Посмотреть логи
sudo journalctl -u halloween-bot -f

# Посмотреть последние 100 строк логов
sudo journalctl -u halloween-bot -n 100

# Отключить автозапуск
sudo systemctl disable halloween-bot
```

## 📊 Мониторинг и логи

### Просмотр логов в реальном времени

```bash
sudo journalctl -u halloween-bot -f
```

### Создание файла логов

Создайте директорию для логов:
```bash
mkdir ~/HalloweenBotPHG/logs
```

Измените `bot.py`, добавив в начало файла (после импортов):

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
```

## 🔒 Безопасность

### Настройка firewall (опционально)

```bash
# Разрешите SSH
sudo ufw allow ssh

# Включите firewall
sudo ufw enable

# Проверьте статус
sudo ufw status
```

### Защита токена бота

Убедитесь, что файл `config.py` недоступен для чтения другим пользователям:

```bash
chmod 600 config.py
```

## 🔄 Обновление бота

Чтобы получить обновления из GitHub:

```bash
# Остановите бота
sudo systemctl stop halloween-bot

# Обновите код
cd ~/HalloweenBotPHG  # или /opt/HalloweenBotPHG
git pull origin main

# Обновите зависимости (если изменились)
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Запустите бота
sudo systemctl start halloween-bot
```

## 🗄️ Резервное копирование базы данных

Создайте скрипт для бэкапа:

```bash
nano ~/backup_bot.sh
```

Вставьте:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp ~/HalloweenBotPHG/contest_bot.db ~/HalloweenBotPHG/backups/contest_bot_$DATE.db
echo "Backup created: contest_bot_$DATE.db"
```

Сделайте исполняемым:
```bash
chmod +x ~/backup_bot.sh
```

Создайте директорию для бэкапов:
```bash
mkdir ~/HalloweenBotPHG/backups
```

Запускайте бэкап:
```bash
~/backup_bot.sh
```

### Автоматический бэкап через cron

```bash
crontab -e
```

Добавьте строку (бэкап каждый день в 3:00):
```
0 3 * * * /home/your_username/backup_bot.sh
```

## ❓ Решение проблем

### Бот не запускается

1. Проверьте логи:
```bash
sudo journalctl -u halloween-bot -n 50
```

2. Проверьте права доступа:
```bash
ls -la ~/HalloweenBotPHG
```

3. Проверьте виртуальное окружение:
```bash
source venv/bin/activate
python3 -c "import aiogram; print('OK')"
```

### База данных заблокирована

```bash
sudo systemctl stop halloween-bot
rm contest_bot.db-wal contest_bot.db-shm
sudo systemctl start halloween-bot
```

### Проблемы с правами доступа

```bash
sudo chown -R your_username:your_username ~/HalloweenBotPHG
chmod 755 ~/HalloweenBotPHG
```

## 📞 Полезные команды

```bash
# Узнать ваше имя пользователя
whoami

# Узнать текущую директорию
pwd

# Проверить использование диска
df -h

# Проверить использование памяти
free -h

# Проверить запущенные процессы Python
ps aux | grep python

# Убить зависший процесс бота
pkill -f bot.py
```

## ✅ Проверка работы

1. Отправьте `/start` вашему боту в Telegram
2. Проверьте, что бот отвечает
3. Попробуйте пройти регистрацию
4. Проверьте, что заявка приходит в модераторский чат
5. Проверьте команду `/stats` в модераторском чате

## 🎉 Готово!

Ваш бот успешно установлен и запущен на Ubuntu 20.04!

Для поддержки обращайтесь к документации: https://github.com/Mafyan/HalloweenBotPHG

