
from utils.menu_handlers import *
from bot_config import bot  # Проверьте, что bot импортируется правильно
from database_utils import *
import sqlite3
from telebot import types

back = '🔙 Back'
casino_players = {}


def get_balance(chat_id):
    """Получение баланса пользователя из базы данных."""
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT balance FROM casino_users WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        return None
    except Exception as e:
        print(f"Ошибка в get_balance: {e}")
        return None


def get_db_connection(message):
    """Получение соединения с базой данных."""
    connection = sqlite3.connect(db_path)
    return connection


def get_first_name(chat_id):
    """Получение имени пользователя из базы данных."""
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT first_name FROM casino_users WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        return "User"  # Если имени нет
    except Exception as e:
        print(f"Ошибка в get_first_name: {e}")
        return "User"


def update_first_name(chat_id, new_first_name):
    """Обновление имени пользователя в базе данных."""
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('UPDATE casino_users SET first_name = ? WHERE chat_id = ?', (new_first_name, chat_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Ошибка в update_first_name: {e}")


def my_profile(chat_id):
    """Формирование и отправка профиля пользователя."""
    try:
        first_name = escape_markdown(get_first_name(chat_id))
        user_balance = escape_markdown(str(get_balance(chat_id)))
        intellect = get_intelligence_points_by_chat_id(chat_id)
        caption = f"""
🖼 **Your name:** {first_name}
💳 **Your balance:** {user_balance} 💰
🧠 **Your Intellect:** {intellect} points
"""

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton("✏️ Edit Profile Name", callback_data="edit_profile_name"),
            types.InlineKeyboardButton("🔙 Back", callback_data="back")
        )

        user_photo = get_user_photo(chat_id)
        if user_photo:
            bot.send_photo(chat_id, user_photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, caption, reply_markup=keyboard, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка в my_profile: {e}")



def get_user_photo(chat_id):
    """Пытаемся получить фотографию пользователя."""
    try:
        user_photos = bot.get_user_profile_photos(chat_id)
        if user_photos.photos:  # Если фотографии найдены
            file_id = user_photos.photos[0][-1].file_id  # Получаем фото с максимальным разрешением
            return file_id
        return None  # Если у пользователя нет фотографии
    except Exception as e:
        print(f"Ошибка в get_user_photo: {e}")
        return None


# Изменение имени



def name_exists(new_name):
    """Проверяем, существует ли имя в базе данных."""
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM casino_users WHERE first_name = ?)', (new_name,))
        result = cursor.fetchone()
        connection.close()
        print(f"[LOG] Проверка доступности имени '{new_name}': {'занято' if result[0] == 1 else 'свободно'}")
        return result[0] == 1
    except Exception as e:
        print(f"[ERROR] Ошибка в name_exists: {e}")
        return False



def escape_markdown(text):
    """Экранируем символы Markdown."""
    escape_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_characters:
        text = text.replace(char, f'\\{char}')
    return text




