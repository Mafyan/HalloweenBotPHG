"""
Главный файл бота для конкурса фотографий
"""
import asyncio
import re
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import Database

# Инициализация
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database(config.DATABASE_FILE)


# Определение состояний FSM
class ContestStates(StatesGroup):
    choosing_club = State()
    accepting_consent = State()
    waiting_phone = State()
    waiting_photo = State()


def is_deadline_passed() -> bool:
    """Проверка, прошёл ли дедлайн"""
    accepting = db.get_bot_state('accepting_submissions')
    if accepting == 'false':
        return True
    
    now = datetime.now(config.TIMEZONE)
    return now > config.DEADLINE


def format_phone(phone: str) -> str:
    """Форматирование номера телефона"""
    # Удаляем все кроме цифр и +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Если начинается с 8, заменяем на +7
    if phone.startswith('8'):
        phone = '+7' + phone[1:]
    elif phone.startswith('7') and not phone.startswith('+7'):
        phone = '+7' + phone[1:]
    elif not phone.startswith('+'):
        phone = '+' + phone
    
    return phone


def validate_phone(phone: str) -> bool:
    """Валидация номера телефона в формате E.164"""
    phone = format_phone(phone)
    # Проверяем формат E.164: +, затем 10-15 цифр
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, phone))


# Клавиатуры
def get_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для начала"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Участвовать 🎃", callback_data="participate")]
    ])
    return keyboard


def get_clubs_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора клуба"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="FITCLUB Лихоборы", callback_data="club_lihobory")],
        [InlineKeyboardButton(text="FITCLUB Селигерская", callback_data="club_seligerskaya")]
    ])
    return keyboard


def get_consent_keyboard(club: str) -> InlineKeyboardMarkup:
    """Клавиатура согласия на обработку данных"""
    data_url = config.CLUBS[club]["data_url"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Политика обработки данных", url=data_url)],
        [InlineKeyboardButton(text="Соглашаюсь ✅", callback_data="consent_agree")],
        [InlineKeyboardButton(text="Отмена", callback_data="consent_cancel")]
    ])
    return keyboard


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для отправки номера телефона"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Поделиться номером", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_moderation_keyboard(submission_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для модерации"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{submission_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{submission_id}")
        ]
    ])
    return keyboard


# Хендлер команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработка команды /start"""
    # Проверяем, не отправлял ли пользователь уже заявку
    if db.has_user_submitted(message.from_user.id):
        await message.answer(
            "✅ Вы уже отправили заявку на конкурс!\n\n"
            "Ваша заявка находится на модерации. "
            "После проверки ваше фото будет опубликовано для голосования.\n\n"
            f"📢 Следите за новостями в канале {config.VOTING_CHANNEL}"
        )
        return
    
    await state.clear()
    
    if is_deadline_passed():
        await message.answer(
            "⏰ Приём заявок завершён.\n\n"
            f"Голосование с 1 по 4 ноября в канале {config.VOTING_CHANNEL}"
        )
        return
    
    welcome_text = (
        "🎃 Привет! Добро пожаловать на конкурс костюмов Хэллоуин!\n\n"
        "📸 Отправьте ваше фото в костюме из нашей фотозоны для участия в конкурсе!\n\n"
        "Правила просты:\n"
        "• Сделайте фото в костюме в нашей фотозоне\n"
        "• Отправьте фото через этого бота\n"
        "• Пройдите простую регистрацию\n"
        "• Ждите модерации\n\n"
        "Готовы участвовать? Нажмите кнопку ниже! 👇"
    )
    
    await message.answer(welcome_text, reply_markup=get_start_keyboard())


# Хендлер кнопки "Участвовать"
@dp.callback_query(F.data == "participate")
async def process_participate(callback: CallbackQuery, state: FSMContext):
    """Обработка кнопки Участвовать"""
    if is_deadline_passed():
        await callback.message.edit_text(
            "⏰ Приём заявок завершён.\n\n"
            f"Голосование с 1 по 4 ноября в канале {config.VOTING_CHANNEL}"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "Выберите ваш клуб:",
        reply_markup=get_clubs_keyboard()
    )
    await state.set_state(ContestStates.choosing_club)
    await callback.answer()


# Хендлер выбора клуба
@dp.callback_query(ContestStates.choosing_club, F.data.startswith("club_"))
async def process_club_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора клуба"""
    club = callback.data.replace("club_", "")
    club_name = config.CLUBS[club]["name"]
    
    await state.update_data(club=club, club_name=club_name)
    
    await callback.message.edit_text(
        f"Вы выбрали: {club_name}\n\n"
        "Для участия в конкурсе необходимо согласие на обработку персональных данных.\n\n"
        "Пожалуйста, ознакомьтесь с политикой обработки данных и дайте своё согласие:",
        reply_markup=get_consent_keyboard(club)
    )
    await state.set_state(ContestStates.accepting_consent)
    await callback.answer()


# Хендлер согласия на обработку данных
@dp.callback_query(ContestStates.accepting_consent, F.data == "consent_agree")
async def process_consent_agree(callback: CallbackQuery, state: FSMContext):
    """Обработка согласия"""
    await callback.message.edit_text(
        "✅ Спасибо за согласие!\n\n"
        "Теперь поделитесь вашим номером телефона.\n\n"
        "Вы можете:\n"
        "• Нажать кнопку \"📲 Поделиться номером\"\n"
        "• Или ввести номер вручную в формате +7XXXXXXXXXX"
    )
    
    await callback.message.answer(
        "Нажмите кнопку ниже для отправки номера телефона:",
        reply_markup=get_phone_keyboard()
    )
    
    await state.set_state(ContestStates.waiting_phone)
    await callback.answer()


@dp.callback_query(ContestStates.accepting_consent, F.data == "consent_cancel")
async def process_consent_cancel(callback: CallbackQuery, state: FSMContext):
    """Обработка отмены согласия"""
    await callback.message.edit_text(
        "❌ Без согласия на обработку персональных данных участие в конкурсе невозможно.\n\n"
        "Если передумаете, используйте команду /start для начала заново."
    )
    await state.clear()
    await callback.answer()


# Хендлер получения номера телефона через кнопку
@dp.message(ContestStates.waiting_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Обработка номера телефона через contact"""
    phone = format_phone(message.contact.phone_number)
    
    await state.update_data(phone=phone)
    await message.answer(
        f"✅ Номер телефона получен: {phone}\n\n"
        "📸 Теперь отправьте ваше фото в костюме!\n\n"
        "⚠️ Важно: отправьте фото как изображение (не файл или документ).",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ContestStates.waiting_photo)


# Хендлер ручного ввода номера телефона
@dp.message(ContestStates.waiting_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    """Обработка ручного ввода номера телефона"""
    phone_input = message.text
    
    if not validate_phone(phone_input):
        await message.answer(
            "❌ Неверный формат номера телефона.\n\n"
            "Пожалуйста, введите номер в формате:\n"
            "+7XXXXXXXXXX (10-15 цифр)\n\n"
            "Или используйте кнопку \"📲 Поделиться номером\"",
            reply_markup=get_phone_keyboard()
        )
        return
    
    phone = format_phone(phone_input)
    await state.update_data(phone=phone)
    await message.answer(
        f"✅ Номер телефона получен: {phone}\n\n"
        "📸 Теперь отправьте ваше фото в костюме!\n\n"
        "⚠️ Важно: отправьте фото как изображение (не файл или документ).",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ContestStates.waiting_photo)


# Хендлер получения фото
@dp.message(ContestStates.waiting_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Обработка фотографии"""
    if is_deadline_passed():
        await message.answer(
            "⏰ К сожалению, приём заявок завершён.\n\n"
            f"Голосование с 1 по 4 ноября в канале {config.VOTING_CHANNEL}"
        )
        await state.clear()
        return
    
    # Получаем данные из состояния
    data = await state.get_data()
    club = data.get('club')
    club_name = data.get('club_name')
    phone = data.get('phone')
    
    # Получаем информацию о пользователе
    user = message.from_user
    user_id = user.id
    username = user.username or ""
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    
    # Получаем file_id фото (берём самое большое разрешение)
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    
    # Сохраняем в базу данных
    submission_id = db.add_submission(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        club=club,
        phone=phone,
        photo_file_id=photo_file_id
    )
    
    # Формируем сообщение для модераторского чата
    full_name = f"{first_name} {last_name}".strip() or "Без имени"
    username_text = f"@{username}" if username else "нет username"
    
    moderation_text = (
        f"📝 Новая заявка #{submission_id}\n\n"
        f"👤 Имя: {full_name}\n"
        f"🆔 Username: {username_text}\n"
        f"🏢 Клуб: {club_name}\n"
        f"📱 Телефон: {phone}\n"
        f"🆔 User ID: {user_id}"
    )
    
    # Отправляем фото с данными в модераторский чат
    try:
        mod_message = await bot.send_photo(
            chat_id=config.MODERATION_CHAT_ID,
            photo=photo_file_id,
            caption=moderation_text,
            reply_markup=get_moderation_keyboard(submission_id)
        )
        
        # Сохраняем ID сообщения модератора
        db.update_moderator_message(submission_id, mod_message.message_id)
        
    except Exception as e:
        print(f"Ошибка отправки в модераторский чат: {e}")
    
    # Подтверждение пользователю
    await message.answer(
        "✅ Отлично! Ваша заявка успешно принята!\n\n"
        "📝 Что дальше?\n"
        "• Ваше фото отправлено на модерацию\n"
        "• Модераторы проверят заявку в ближайшее время\n"
        "• После одобрения фото будет опубликовано для голосования\n\n"
        f"📢 Следите за новостями и голосованием в канале {config.VOTING_CHANNEL}\n\n"
        "🎃 Спасибо за участие в конкурсе! Удачи!",
        reply_markup=ReplyKeyboardRemove()
    )
    
    await state.clear()


# Хендлер неправильного формата (документ вместо фото)
@dp.message(ContestStates.waiting_photo, F.document | F.video)
async def process_wrong_format(message: Message):
    """Обработка неправильного формата"""
    await message.answer(
        "❌ Пожалуйста, отправьте фото как изображение, а не как файл или документ.\n\n"
        "Для этого при отправке выберите вариант \"Фото\" вместо \"Файл\"."
    )


# Хендлеры модерации
@dp.callback_query(F.data.startswith("approve_"))
async def process_approve(callback: CallbackQuery):
    """Обработка одобрения заявки"""
    submission_id = int(callback.data.replace("approve_", ""))
    moderator_id = callback.from_user.id
    moderator_name = callback.from_user.first_name or "Модератор"
    
    # Обновляем статус в БД
    db.update_submission_status(submission_id, "APPROVED", moderator_id)
    
    # Обновляем сообщение с результатом модерации
    submission = db.get_submission(submission_id)
    if submission:
        updated_caption = (
            f"{callback.message.caption}\n\n"
            f"✅ ОДОБРЕНО\n"
            f"Модератор: {moderator_name}"
        )
        
        try:
            await callback.message.edit_caption(
                caption=updated_caption,
                reply_markup=None
            )
        except:
            pass
    
    await callback.answer("✅ Заявка одобрена!", show_alert=True)


@dp.callback_query(F.data.startswith("reject_"))
async def process_reject(callback: CallbackQuery):
    """Обработка отклонения заявки"""
    submission_id = int(callback.data.replace("reject_", ""))
    moderator_id = callback.from_user.id
    moderator_name = callback.from_user.first_name or "Модератор"
    
    # Обновляем статус в БД
    db.update_submission_status(submission_id, "REJECTED", moderator_id)
    
    # Обновляем сообщение с результатом модерации
    submission = db.get_submission(submission_id)
    if submission:
        updated_caption = (
            f"{callback.message.caption}\n\n"
            f"❌ ОТКЛОНЕНО\n"
            f"Модератор: {moderator_name}"
        )
        
        try:
            await callback.message.edit_caption(
                caption=updated_caption,
                reply_markup=None
            )
        except:
            pass
    
    await callback.answer("❌ Заявка отклонена!", show_alert=True)


# Команда /finish для завершения приёма заявок
@dp.message(Command("finish"))
async def cmd_finish(message: Message):
    """Завершить приём заявок и опубликовать одобренные"""
    # Проверяем, что команду вызвали в модераторском чате
    if message.chat.id != config.MODERATION_CHAT_ID:
        await message.answer("❌ Эта команда доступна только в модераторском чате.")
        return
    
    # Устанавливаем флаг завершения приёма
    db.set_bot_state('accepting_submissions', 'false')
    
    await message.answer("⏰ Приём заявок завершён. Начинаю публикацию одобренных заявок...")
    
    # Получаем все одобренные заявки
    approved = db.get_approved_submissions()
    
    if not approved:
        await message.answer("📭 Нет одобренных заявок для публикации.")
        return
    
    await message.answer(f"📊 Найдено одобренных заявок: {len(approved)}")
    
    # Публикуем каждую заявку
    for idx, submission in enumerate(approved, 1):
        full_name = f"{submission['first_name']} {submission['last_name']}".strip()
        username_text = f"@{submission['username']}" if submission['username'] else ""
        
        caption = (
            f"🎃 Участник #{idx}\n\n"
            f"👤 {full_name}\n"
            f"{username_text}\n"
            f"🏢 {config.CLUBS[submission['club']]['name']}"
        )
        
        try:
            await bot.send_photo(
                chat_id=config.MODERATION_CHAT_ID,
                photo=submission['photo_file_id'],
                caption=caption
            )
            await asyncio.sleep(1)  # Небольшая задержка между отправками
        except Exception as e:
            print(f"Ошибка публикации заявки {submission['id']}: {e}")
    
    # Удаляем отклонённые заявки
    deleted = db.delete_rejected_photos()
    
    stats = db.get_stats()
    
    await message.answer(
        f"✅ Публикация завершена!\n\n"
        f"📊 Статистика:\n"
        f"✅ Одобрено: {stats.get('APPROVED', 0)}\n"
        f"❌ Отклонено (удалено): {deleted}\n"
        f"📥 Всего обработано: {stats.get('APPROVED', 0) + deleted}"
    )


# Команда /stats для статистики
@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """Показать статистику заявок"""
    if message.chat.id != config.MODERATION_CHAT_ID:
        return
    
    stats = db.get_stats()
    
    stats_text = (
        "📊 Статистика заявок:\n\n"
        f"⏳ На модерации: {stats.get('SUBMITTED', 0)}\n"
        f"✅ Одобрено: {stats.get('APPROVED', 0)}\n"
        f"❌ Отклонено: {stats.get('REJECTED', 0)}\n"
        f"📥 Всего: {sum(stats.values())}"
    )
    
    await message.answer(stats_text)


# Универсальный обработчик для пользователей, уже отправивших заявку
@dp.message()
async def handle_already_submitted(message: Message):
    """Обработка сообщений от пользователей, уже отправивших заявку"""
    # Игнорируем сообщения из модераторского чата
    if message.chat.id == config.MODERATION_CHAT_ID:
        return
    
    # Проверяем, отправлял ли пользователь заявку
    if db.has_user_submitted(message.from_user.id):
        await message.answer(
            "✅ Ваша заявка уже принята!\n\n"
            f"📢 Следите за новостями в канале {config.VOTING_CHANNEL}"
        )
    else:
        # Если пользователь не в процессе регистрации и не отправлял заявку
        await message.answer(
            "Для участия в конкурсе используйте команду /start"
        )


async def main():
    """Запуск бота"""
    print("🤖 Бот запущен!")
    print(f"📅 Дедлайн приёма заявок: {config.DEADLINE.strftime('%d.%m.%Y %H:%M')} МСК")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

