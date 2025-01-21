import telebot
from telebot import types
from database_utils import *  # Импорт функции для работы с балансом, если нужна
from bot_config import bot
# Placeholder для глобальной переменной back
back = "⬅ Back"  # Замените это значение на актуальное, если в вашем коде есть переменная `back`


def info(chat_id):
    """Функция для вывода информации о владельце или боте"""
    text = "What information are you looking for?"
    markup = telebot.types.InlineKeyboardMarkup()
    owner = types.InlineKeyboardButton('About Owner', callback_data='owner')
    bot1 = types.InlineKeyboardButton('About Bot', callback_data='bot owner')
    back_to_main = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(owner, bot1)
    markup.row(back_to_main)
    bot.send_message(chat_id, text, reply_markup=markup)


def manas(chat_id):
    """Вывод информации о Manas и сопутствующих сервисах"""
    text = 'The necessary information about Manas is stored here:'
    markup = types.InlineKeyboardMarkup()
    obis_test = types.InlineKeyboardButton('Obis Test 📋', url='https://obistest.manas.edu.kg/site/login')
    manas_food = types.InlineKeyboardButton('Manas Yemek 🍴', url='https://beslenme.manas.edu.kg/menu')
    time_table_manas = types.InlineKeyboardButton('Time Table 🕒', url='http://timetable.manas.edu.kg/department')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(obis_test, manas_food, time_table_manas)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)


def games(chat_id):
    """Функция для вывода игровых возможностей, включая баланс"""
    current_balance = get_balance(chat_id)  # Получение текущего баланса пользователя
    text = (f'*Your balance: {current_balance} 💰*\n\n'
            f'These games are available now: 🎯')
    markup = types.InlineKeyboardMarkup()
    guess_word = types.InlineKeyboardButton('Guess Word 🔮', callback_data='guess_word')
    math_game = types.InlineKeyboardButton('Math Game 🧠', callback_data='math_game')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(guess_word)
    markup.row(math_game)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


def random_things(chat_id):
    """Функция для вывода меню случайных вещей"""
    text = "Choose what random thing you'd like to see 🎲:"
    markup = types.InlineKeyboardMarkup()
    fact = types.InlineKeyboardButton('Random Fact 🧠', callback_data='random_fact')
    motivation = types.InlineKeyboardButton('Random Motivation 💡', callback_data='random_motivation')
    random_photo = types.InlineKeyboardButton('Random Photo 🏞', callback_data='random_photo')
    joke = types.InlineKeyboardButton('Random Joke 😂', callback_data='random_joke')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(fact, motivation)
    markup.row(random_photo, joke)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)
