# 🎮 Команды управления ботом

## 📱 Команды для пользователей

### `/start`
Начать регистрацию на конкурс. Запускает процесс отправки заявки.

**Что происходит:**
- Показывает приветствие и правила
- Проверяет дедлайн (31.10.2025 23:00 МСК)
- Если дедлайн прошёл - показывает сообщение о завершении приёма

---

## 👨‍💼 Команды для модераторов (в модераторском чате)

### `/stats`
Показывает статистику заявок

**Выводит:**
- ⏳ Количество заявок на модерации (SUBMITTED)
- ✅ Количество одобренных заявок (APPROVED)
- ❌ Количество отклонённых заявок (REJECTED)
- 📥 Общее количество заявок

**Пример:**
```
📊 Статистика заявок:

⏳ На модерации: 5
✅ Одобрено: 12
❌ Отклонено: 3
📥 Всего: 20
```

---

### `/finish`
Завершает приём заявок и публикует все одобренные заявки

**Что происходит:**
1. Останавливает приём новых заявок
2. Публикует все одобренные заявки по очереди в модераторский чат
3. Удаляет отклонённые заявки из базы данных
4. Показывает финальную статистику

**Важно:** После выполнения этой команды новые заявки приниматься не будут!

**Пример вывода:**
```
⏰ Приём заявок завершён. Начинаю публикацию одобренных заявок...
📊 Найдено одобренных заявок: 15

[Публикует все одобренные заявки с фото]

✅ Публикация завершена!

📊 Статистика:
✅ Одобрено: 15
❌ Отклонено (удалено): 3
📥 Всего обработано: 18
```

---

## 🔘 Кнопки модерации

Появляются под каждой заявкой в модераторском чате:

### ✅ Одобрить
- Устанавливает статус заявки: `APPROVED`
- Сохраняет заявку для публикации
- Убирает кнопки модерации
- Показывает модератора, который одобрил

### ❌ Отклонить
- Устанавливает статус заявки: `REJECTED`
- Помечает заявку для удаления
- Убирает кнопки модерации
- Показывает модератора, который отклонил

---

## 🖥️ Команды управления сервером Ubuntu

### Запуск бота

#### Через systemd (рекомендуется):
```bash
sudo systemctl start halloween-bot
```

#### Через screen:
```bash
screen -S halloween_bot
source ~/HalloweenBotPHG/venv/bin/activate
python3 bot.py
# Выход: Ctrl+A, затем D
```

#### Напрямую (для тестирования):
```bash
cd ~/HalloweenBotPHG
source venv/bin/activate
python3 bot.py
# Остановка: Ctrl+C
```

---

### Остановка бота

#### Через systemd:
```bash
sudo systemctl stop halloween-bot
```

#### Через screen:
```bash
screen -r halloween_bot
# В открывшейся сессии: Ctrl+C
```

#### Найти и убить процесс:
```bash
ps aux | grep bot.py
kill [PID]
```

---

### Перезапуск бота

#### Через systemd:
```bash
sudo systemctl restart halloween-bot
```

#### Через screen:
```bash
screen -r halloween_bot
# Ctrl+C для остановки
python3 bot.py
# Ctrl+A, затем D для выхода
```

---

### Проверка статуса

#### Через systemd:
```bash
# Полный статус
sudo systemctl status halloween-bot

# Только проверка работает ли
sudo systemctl is-active halloween-bot

# Включён ли автозапуск
sudo systemctl is-enabled halloween-bot
```

#### Через screen:
```bash
# Список всех сессий screen
screen -ls

# Подключиться к сессии
screen -r halloween_bot
```

#### Проверка процесса:
```bash
ps aux | grep bot.py
```

---

### Просмотр логов

#### Через systemd:
```bash
# Последние 50 строк
sudo journalctl -u halloween-bot -n 50

# Последние 100 строк
sudo journalctl -u halloween-bot -n 100

# В реальном времени (live)
sudo journalctl -u halloween-bot -f

# За последний час
sudo journalctl -u halloween-bot --since "1 hour ago"

# За сегодня
sudo journalctl -u halloween-bot --since today

# За определённую дату
sudo journalctl -u halloween-bot --since "2025-10-21 00:00:00"
```

#### Через screen:
```bash
# Подключиться к сессии и увидеть вывод
screen -r halloween_bot
```

---

### Включение/отключение автозапуска

```bash
# Включить автозапуск при загрузке системы
sudo systemctl enable halloween-bot

# Отключить автозапуск
sudo systemctl disable halloween-bot
```

---

### Обновление бота

```bash
# 1. Остановить бота
sudo systemctl stop halloween-bot

# 2. Перейти в папку проекта
cd ~/HalloweenBotPHG

# 3. Получить обновления с GitHub
git pull origin main

# 4. Активировать виртуальное окружение
source venv/bin/activate

# 5. Обновить зависимости (если изменились)
pip install -r requirements.txt --upgrade

# 6. Запустить бота снова
sudo systemctl start halloween-bot

# 7. Проверить статус
sudo systemctl status halloween-bot
```

---

### Резервное копирование базы данных

```bash
# Создать папку для бэкапов
mkdir -p ~/backups

# Ручное копирование
cp ~/HalloweenBotPHG/contest_bot.db ~/backups/contest_bot_$(date +%Y%m%d_%H%M%S).db

# Просмотр бэкапов
ls -lh ~/backups/
```

---

### Просмотр базы данных

```bash
cd ~/HalloweenBotPHG
sqlite3 contest_bot.db

# В SQLite консоли:
.tables                          # Показать все таблицы
SELECT * FROM submissions;       # Показать все заявки
SELECT COUNT(*) FROM submissions; # Количество заявок
.quit                            # Выход
```

---

### Полная переустановка бота

```bash
# 1. Остановить бота
sudo systemctl stop halloween-bot
sudo systemctl disable halloween-bot

# 2. Сделать бэкап базы данных
cp ~/HalloweenBotPHG/contest_bot.db ~/contest_bot_backup.db

# 3. Удалить старую версию
rm -rf ~/HalloweenBotPHG

# 4. Клонировать заново
git clone https://github.com/Mafyan/HalloweenBotPHG.git
cd HalloweenBotPHG

# 5. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 6. Установить зависимости
pip install -r requirements.txt

# 7. Восстановить базу данных (если нужно)
cp ~/contest_bot_backup.db ~/HalloweenBotPHG/contest_bot.db

# 8. Запустить бота
sudo systemctl start halloween-bot
sudo systemctl enable halloween-bot
```

---

## 🔍 Диагностика проблем

### Бот не запускается

```bash
# Проверить логи на ошибки
sudo journalctl -u halloween-bot -n 100

# Проверить конфигурацию
cat ~/HalloweenBotPHG/config.py

# Проверить права на файлы
ls -la ~/HalloweenBotPHG/

# Попробовать запустить вручную
cd ~/HalloweenBotPHG
source venv/bin/activate
python3 bot.py
```

### Бот не отвечает в Telegram

```bash
# Проверить, что бот запущен
sudo systemctl status halloween-bot

# Проверить подключение к интернету
ping -c 3 telegram.org

# Проверить токен бота в config.py
cat ~/HalloweenBotPHG/config.py | grep BOT_TOKEN
```

### Высокое использование памяти/CPU

```bash
# Проверить использование ресурсов
top -p $(pgrep -f bot.py)

# Или через htop (если установлен)
htop -p $(pgrep -f bot.py)
```

---

## 📊 Мониторинг

### Проверка работоспособности

```bash
# Быстрая проверка всего
systemctl is-active halloween-bot && echo "✅ Бот работает" || echo "❌ Бот остановлен"

# Проверка использования диска
df -h ~/HalloweenBotPHG/

# Размер базы данных
ls -lh ~/HalloweenBotPHG/contest_bot.db
```

---

## 🚨 Экстренные команды

### Принудительная остановка
```bash
sudo systemctl stop halloween-bot
sudo pkill -f bot.py
```

### Очистка всех данных (ОСТОРОЖНО!)
```bash
# Создайте бэкап перед этим!
sudo systemctl stop halloween-bot
rm ~/HalloweenBotPHG/contest_bot.db
```

### Сброс к начальному состоянию
```bash
sudo systemctl stop halloween-bot
cd ~/HalloweenBotPHG
git reset --hard origin/main
git pull origin main
sudo systemctl start halloween-bot
```

---

## 📞 Горячие комбинации клавиш

### В терминале:
- `Ctrl+C` - остановить текущий процесс (бота)
- `Ctrl+Z` - приостановить процесс
- `Ctrl+D` - выход из виртуального окружения/терминала

### В screen:
- `Ctrl+A` затем `D` - отключиться от сессии (detach)
- `Ctrl+A` затем `K` - убить сессию
- `Ctrl+A` затем `[` - режим прокрутки (выход: `Esc`)

### В nano (редакторе):
- `Ctrl+O` - сохранить файл
- `Ctrl+X` - выход
- `Ctrl+K` - вырезать строку
- `Ctrl+U` - вставить

---

## 🎯 Быстрые команды (шпаргалка)

```bash
# Статус
sudo systemctl status halloween-bot

# Запуск/Остановка/Перезапуск
sudo systemctl start halloween-bot
sudo systemctl stop halloween-bot
sudo systemctl restart halloween-bot

# Логи
sudo journalctl -u halloween-bot -f

# Обновление
cd ~/HalloweenBotPHG && git pull && sudo systemctl restart halloween-bot

# Бэкап
cp ~/HalloweenBotPHG/contest_bot.db ~/backups/contest_bot_$(date +%Y%m%d).db
```

