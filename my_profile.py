import telebot
import random
import sqlite3
from telebot import types, callback_data
import time
import requests
import threading
bot = telebot.TeleBot('7244608311:AAHrlYJnzHwBpTTZ1Js7QG6gBTwDxtmx3Yw')
db_path = 'casino.db'

back = '🔙 Back'
casino_players = {}
def send_menu(message):
    text = '*WELCOME*'
    markup = types.InlineKeyboardMarkup()
    my_profile= types.InlineKeyboardButton('My Profile', callback_data='my_profile')
    markup.add(my_profile)
    bot.send_message(message.chat.id, text, reply_markup=markup,parse_mode="Markdown")
@bot.message_handler(commands=['start'])
def send_menu1(message):
    send_menu(message)

def get_balance(chat_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM casino_users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return None

def get_db_connection(message):
    connection = sqlite3.connect(db_path)
    return connection
def get_first_name(chat_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT first_name FROM casino_users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return "User"  # Если имени нет
def update_first_name(chat_id, new_first_name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('UPDATE casino_users SET first_name = ? WHERE chat_id = ?', (new_first_name, chat_id))
    connection.commit()
    connection.close()
def my_profile(chat_id):
    """Формирование и отправка профиля пользователя."""
    # Получаем данные пользователя из базы
    first_name = escape_markdown(get_first_name(chat_id))  # Экранируем имя
    user_balance = escape_markdown(str(get_balance(chat_id)))  # Экранируем баланс (преобразуем в строку)

    # Форматируем текст
    caption = f"""
🖼 **Имя:** {first_name}
💳 **Баланс:** {user_balance} ₽
"""

    # Кнопки
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("✏️ Edit Profile Name", callback_data="edit_profile_name"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")
    )

    # Получаем фото пользователя
    user_photo = get_user_photo(chat_id)

    if user_photo:  # Если фотография есть
        bot.send_photo(chat_id, user_photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, caption, reply_markup=keyboard, parse_mode="Markdown")


def get_user_photo(chat_id):
    user_photos = bot.get_user_profile_photos(chat_id)
    if user_photos.photos:  # Если найдены фото профиля
        file_id = user_photos.photos[0][-1].file_id  # Берем фото с максимальным разрешением
        return file_id
    return None  # Если у пользователя нет фотографии



# --- Обработчик для команды my_profile
@bot.callback_query_handler(func=lambda call: call.data == 'my_profile')
def my_profile_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  # Удаляем предыдущее сообщение
    my_profile(call.message.chat.id)  # Открываем профиль пользователя


# Изменение имени
@bot.callback_query_handler(func=lambda call: call.data == "edit_profile_name")
def edit_profile_name_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  # Удаляем текущее сообщение
    bot.send_message(call.message.chat.id, "Пожалуйста, введите новое имя:")
    bot.register_next_step_handler(call.message, process_new_name)


def name_exists(new_name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT EXISTS(SELECT 1 FROM casino_users WHERE first_name = ?)', (new_name,))
    result = cursor.fetchone()
    connection.close()
    return result[0] == 1  # Если пользователь существует, вернется 1, иначе 0
def escape_markdown(text):
    """Функция для экранирования символов Markdown."""
    escape_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_characters:
        text = text.replace(char, f'\\{char}')
    return text

def process_new_name(message):
    new_name = message.text.strip()  # Получаем новое имя и убираем лишние пробелы
    chat_id = message.chat.id

    if name_exists(new_name):
        bot.send_message(chat_id, f"Имя **{escape_markdown(new_name)}** уже занято. Введите другое имя:",
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, process_new_name)
    else:
        update_first_name(chat_id, new_name)
        bot.send_message(chat_id, f"Ваше имя успешно обновлено на **{escape_markdown(new_name)}**!",
                         parse_mode="Markdown")
        my_profile(chat_id)



@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    send_menu(call.message)  # Возвращаем пользователя в главное меню



def send_menu(message):
    text = '*WELCOME*'
    markup = types.InlineKeyboardMarkup()
    my_profile_button = types.InlineKeyboardButton('Profile', callback_data='my_profile')
    markup.add(my_profile_button)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def send_menu_start(message):
    send_menu(message)


# Запуск бота
bot.polling(none_stop=True)


