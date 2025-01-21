from telebot import types
from database_utils import get_balance, update_balance

back = '🔙 Back'
casino_players = {}


def send_menu(chat_id, bot):
    """Отправка главного меню бота"""
    text = "Choose an option 📲. We have everything to make you happy!"
    casino_players[chat_id] = chat_id

    markup = types.InlineKeyboardMarkup()
    my_profile = types.InlineKeyboardButton('MY PROFILE ℹ️', callback_data='my_profile')
    info = types.InlineKeyboardButton('INFO 📋', callback_data='info')
    manas = types.InlineKeyboardButton('MANAS 🎓', callback_data='manas')
    games = types.InlineKeyboardButton('GAMES 👾', callback_data='games')
    random_things = types.InlineKeyboardButton('RANDOM THINGS 🎲', callback_data='random_play')
    gtp_button = types.InlineKeyboardButton('Free Chat GPT ⚪', callback_data='gpt')
    forbes = types.InlineKeyboardButton('FORBES 💸', callback_data='forbes')

    markup.row(my_profile)
    markup.row(info, manas)
    markup.row(games, random_things)
    casino = types.InlineKeyboardButton('CASINO 🎰', callback_data='casino')
    markup.row(casino,forbes)
    markup.row(gtp_button)
    bot.send_message(chat_id, text, reply_markup=markup)


def info_menu(bot, chat_id):
    """Загрузка меню информации"""
    text = "What information are you looking for?"
    markup = types.InlineKeyboardMarkup()
    owner = types.InlineKeyboardButton('About Owner', callback_data='owner')
    bot1 = types.InlineKeyboardButton('About Bot', callback_data='bot owner')
    back_to_main = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(owner, bot1)
    markup.row(back_to_main)
    bot.send_message(chat_id, text, reply_markup=markup)


def manas_menu(bot, chat_id):
    """Меню Manas информации"""
    text = 'The necessary information about Manas is stored here:'
    markup = types.InlineKeyboardMarkup()
    obis_test = types.InlineKeyboardButton('Obis Test 📋', url='https://obistest.manas.edu.kg/site/login')
    manas_food = types.InlineKeyboardButton('Manas Yemek 🍴', url='https://beslenme.manas.edu.kg/menu')
    time_table_manas = types.InlineKeyboardButton('Time Table 🕒', url='http://timetable.manas.edu.kg/department')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(obis_test, manas_food, time_table_manas)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)

