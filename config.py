"""
Конфигурация бота для конкурса фотографий
"""
from datetime import datetime
import pytz

# Telegram настройки
BOT_TOKEN = "7966890729:AAGB3jxzFQkvA7wGsw2iaO-2Z_nUHL3Vq0I"
MODERATION_CHAT_ID = -1003100500797

# Временная зона
TIMEZONE = pytz.timezone('Europe/Moscow')

# Дедлайн для приёма заявок: 31 октября 2025, 23:00 МСК
DEADLINE = TIMEZONE.localize(datetime(2025, 10, 31, 23, 0, 0))

# Клубы
CLUBS = {
    "lihobory": {
        "name": "FITCLUB Лихоборы",
        "data_url": "https://fitclub-moscow.ru/lihobory/data"
    },
    "seligerskaya": {
        "name": "FITCLUB Селигерская",
        "data_url": "https://fitclub-moscow.ru/data"
    }
}

# Канал для голосования
VOTING_CHANNEL = "t.me/fitclubmoscow"

# База данных
DATABASE_FILE = "contest_bot.db"

