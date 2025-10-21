# 🚀 Быстрая шпаргалка по управлению ботом

## 📱 Команды бота в Telegram

### Для пользователей:
- `/start` - начать участие в конкурсе

### Для модераторов (в модераторском чате):
- `/stats` - показать статистику заявок
- `/finish` - завершить конкурс и опубликовать одобренные заявки

### Кнопки модерации:
- **✅ Одобрить** - одобрить заявку
- **❌ Отклонить** - отклонить заявку

---

## 🖥️ Управление на сервере Ubuntu

### 🔄 Основные команды

```bash
# Запуск
sudo systemctl start halloween-bot

# Остановка
sudo systemctl stop halloween-bot

# Перезапуск
sudo systemctl restart halloween-bot

# Статус
sudo systemctl status halloween-bot
```

### 📊 Просмотр логов

```bash
# Последние 50 строк
sudo journalctl -u halloween-bot -n 50

# В реальном времени
sudo journalctl -u halloween-bot -f

# За последний час
sudo journalctl -u halloween-bot --since "1 hour ago"
```

### 🔄 Обновление бота

```bash
cd ~/HalloweenBotPHG
sudo systemctl stop halloween-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl start halloween-bot
```

### 💾 Бэкап базы данных

```bash
# Создать бэкап
cp ~/HalloweenBotPHG/contest_bot.db ~/backups/contest_bot_$(date +%Y%m%d).db

# Просмотр бэкапов
ls -lh ~/backups/
```

### 🔍 Проверка работы

```bash
# Проверить, работает ли бот
sudo systemctl is-active halloween-bot

# Проверить процесс
ps aux | grep bot.py

# Проверить подключение к Telegram
ping -c 3 telegram.org
```

---

## 🆘 Если что-то пошло не так

### Бот не запускается

```bash
# Смотрим логи
sudo journalctl -u halloween-bot -n 100

# Проверяем конфигурацию
cat ~/HalloweenBotPHG/config.py

# Пробуем запустить вручную
cd ~/HalloweenBotPHG
source venv/bin/activate
python3 bot.py
```

### Принудительная остановка

```bash
sudo systemctl stop halloween-bot
sudo pkill -f bot.py
```

### Полная переустановка

```bash
# Бэкап базы
cp ~/HalloweenBotPHG/contest_bot.db ~/contest_bot_backup.db

# Удаление и установка заново
rm -rf ~/HalloweenBotPHG
git clone https://github.com/Mafyan/HalloweenBotPHG.git
cd HalloweenBotPHG
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Восстановление базы
cp ~/contest_bot_backup.db ~/HalloweenBotPHG/contest_bot.db

# Запуск
sudo systemctl start halloween-bot
```

---

## 📚 Полная документация

- **[BOT_COMMANDS.md](BOT_COMMANDS.md)** - полное описание всех команд и операций
- **[UBUNTU_INSTALL.md](UBUNTU_INSTALL.md)** - подробная инструкция по установке на Ubuntu
- **[README.md](README.md)** - общая информация о проекте

---

## 📞 Быстрые проверки

```bash
# Всё в одной команде - проверка статуса
systemctl is-active halloween-bot && echo "✅ Работает" || echo "❌ Остановлен"

# Последние ошибки
sudo journalctl -u halloween-bot -p err -n 20

# Размер базы данных
ls -lh ~/HalloweenBotPHG/contest_bot.db
```

---

## 🎯 Типичные сценарии

### Перезапуск после изменений в коде
```bash
sudo systemctl restart halloween-bot && sudo journalctl -u halloween-bot -f
```

### Проверка работоспособности
```bash
sudo systemctl status halloween-bot | grep Active
```

### Смотреть логи и искать ошибки
```bash
sudo journalctl -u halloween-bot -n 200 | grep -i error
```

---

**Автор:** Halloween Contest Bot  
**Репозиторий:** https://github.com/Mafyan/HalloweenBotPHG

