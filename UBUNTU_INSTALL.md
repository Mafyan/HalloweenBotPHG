# 🐧 Установка бота на Ubuntu 20.04

Подробная инструкция по установке и запуску Telegram бота для конкурса фотографий на сервере Ubuntu 20.04.

## 📋 Предварительные требования

- Сервер Ubuntu 20.04
- Доступ к серверу через SSH
- Права sudo
- Интернет-соединение

## 🚀 Установка

### Шаг 1: Обновление системы

```bash
sudo apt update
sudo apt upgrade -y
```

### Шаг 2: Установка Python и необходимых пакетов

```bash
# Установка Python 3.9 и pip
sudo apt install python3 python3-pip python3-venv git -y

# Проверка версии Python (должна быть 3.8+)
python3 --version
```

### Шаг 3: Клонирование репозитория

```bash
# Переход в домашнюю директорию
cd ~

# Клонирование репозитория
git clone https://github.com/Mafyan/HalloweenBotPHG.git

# Переход в папку проекта
cd HalloweenBotPHG
```

### Шаг 4: Создание виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# После активации в начале строки появится (venv)
```

### Шаг 5: Установка зависимостей

```bash
# Установка всех необходимых пакетов
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 6: Настройка конфигурации (опционально)

Если нужно изменить настройки, отредактируйте файл `config.py`:

```bash
nano config.py
```

Основные параметры уже настроены:
- `BOT_TOKEN` - токен бота
- `MODERATION_CHAT_ID` - ID модераторского чата
- `DEADLINE` - дедлайн приёма заявок

Для сохранения: `Ctrl+O`, `Enter`, для выхода: `Ctrl+X`

## ▶️ Запуск бота

### Разовый запуск (для тестирования)

```bash
# Убедитесь, что виртуальное окружение активно (должно быть (venv) в начале строки)
source venv/bin/activate

# Запуск бота
python3 bot.py
```

Для остановки нажмите `Ctrl+C`

### Запуск в фоновом режиме с помощью screen

```bash
# Установка screen (если не установлен)
sudo apt install screen -y

# Создание новой сессии screen
screen -S halloween_bot

# Активация виртуального окружения
source ~/HalloweenBotPHG/venv/bin/activate

# Запуск бота
python3 ~/HalloweenBotPHG/bot.py
```

Для выхода из screen без остановки бота: `Ctrl+A`, затем `D`

Для возврата к сессии:
```bash
screen -r halloween_bot
```

Для просмотра всех сессий:
```bash
screen -ls
```

### Запуск с помощью systemd (рекомендуется для production)

Создайте systemd service:

```bash
sudo nano /etc/systemd/system/halloween-bot.service
```

Вставьте следующий текст (замените `USERNAME` на ваше имя пользователя):

```ini
[Unit]
Description=Halloween Contest Telegram Bot
After=network.target

[Service]
Type=simple
User=USERNAME
WorkingDirectory=/home/USERNAME/HalloweenBotPHG
Environment="PATH=/home/USERNAME/HalloweenBotPHG/venv/bin"
ExecStart=/home/USERNAME/HalloweenBotPHG/venv/bin/python3 /home/USERNAME/HalloweenBotPHG/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохраните файл (`Ctrl+O`, `Enter`, `Ctrl+X`) и выполните:

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Запуск сервиса
sudo systemctl start halloween-bot

# Включение автозапуска при загрузке системы
sudo systemctl enable halloween-bot

# Проверка статуса
sudo systemctl status halloween-bot
```

#### Управление сервисом:

```bash
# Остановка бота
sudo systemctl stop halloween-bot

# Перезапуск бота
sudo systemctl restart halloween-bot

# Просмотр логов
sudo journalctl -u halloween-bot -f

# Просмотр последних 100 строк логов
sudo journalctl -u halloween-bot -n 100
```

## 🔄 Обновление бота

```bash
# Переход в папку проекта
cd ~/HalloweenBotPHG

# Остановка бота (если используется systemd)
sudo systemctl stop halloween-bot

# Получение последних изменений
git pull origin main

# Активация виртуального окружения
source venv/bin/activate

# Обновление зависимостей (если были изменения)
pip install -r requirements.txt --upgrade

# Запуск бота снова
sudo systemctl start halloween-bot

# Проверка статуса
sudo systemctl status halloween-bot
```

## 📊 Мониторинг и логи

### Просмотр логов в реальном времени:

```bash
# Если используется systemd
sudo journalctl -u halloween-bot -f

# Если используется screen
screen -r halloween_bot
```

### Проверка работы бота:

1. Отправьте боту команду `/start` в Telegram
2. Проверьте, что бот отвечает
3. В модераторском чате выполните команду `/stats` для проверки статистики

## 🔧 Устранение неполадок

### Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u halloween-bot -n 50

# Проверьте, что все зависимости установлены
source ~/HalloweenBotPHG/venv/bin/activate
pip install -r requirements.txt
```

### Проблемы с правами доступа

```bash
# Убедитесь, что файлы принадлежат вашему пользователю
cd ~/HalloweenBotPHG
ls -la

# Если нужно, измените владельца
sudo chown -R $USER:$USER ~/HalloweenBotPHG
```

### Бот не может создать базу данных

```bash
# Проверьте права на запись в директории
cd ~/HalloweenBotPHG
ls -la

# Создайте базу вручную (она создастся автоматически при первом запуске)
touch contest_bot.db
chmod 644 contest_bot.db
```

### Проверка подключения к Telegram API

```bash
# Активируйте виртуальное окружение
source ~/HalloweenBotPHG/venv/bin/activate

# Запустите бота в режиме отладки
python3 bot.py
```

## 🔒 Безопасность

### Рекомендации:

1. **Настройте файрволл:**
```bash
sudo ufw allow OpenSSH
sudo ufw enable
```

2. **Регулярно обновляйте систему:**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Создайте бэкап базы данных:**
```bash
# Создайте папку для бэкапов
mkdir -p ~/backups

# Создайте скрипт для бэкапа
cat > ~/backup-bot.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp ~/HalloweenBotPHG/contest_bot.db ~/backups/contest_bot_$DATE.db
echo "Backup created: contest_bot_$DATE.db"
EOF

# Сделайте скрипт исполняемым
chmod +x ~/backup-bot.sh

# Запуск бэкапа
~/backup-bot.sh
```

4. **Настройте автоматический бэкап через cron:**
```bash
# Откройте crontab
crontab -e

# Добавьте строку для ежедневного бэкапа в 3:00
0 3 * * * /home/$USER/backup-bot.sh
```

## 📱 Проверка работоспособности

После установки проверьте:

1. ✅ Бот отвечает на `/start`
2. ✅ Можно пройти весь процесс регистрации
3. ✅ Фото отправляется в модераторский чат
4. ✅ Кнопки одобрения/отклонения работают
5. ✅ Команда `/stats` показывает статистику
6. ✅ База данных создалась (`contest_bot.db`)

## 💡 Полезные команды

```bash
# Просмотр процессов Python
ps aux | grep python

# Проверка использования памяти
free -h

# Проверка места на диске
df -h

# Просмотр сетевых соединений бота
sudo netstat -tulpn | grep python

# Перезагрузка сервера (если нужно)
sudo reboot
```

## 📞 Поддержка

При возникновении проблем проверьте:
1. Логи бота: `sudo journalctl -u halloween-bot -n 100`
2. Наличие интернет-соединения: `ping -c 3 telegram.org`
3. Правильность токена бота в `config.py`
4. Права бота в модераторском чате Telegram

## 🎉 Готово!

Ваш бот установлен и работает! Теперь он:
- ✅ Автоматически запускается при перезагрузке сервера
- ✅ Перезапускается при сбоях
- ✅ Логирует все действия
- ✅ Готов принимать заявки на конкурс

---

**Важно:** Не забудьте добавить бота в модераторский чат и дать ему права администратора для отправки сообщений!

