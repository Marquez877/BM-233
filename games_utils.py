import random
from telebot import types
from database_utils import get_balance, update_balance
from bot_config import bot
# === [1] GUESS WORD GAME === #
WORDS = [
    "ability", "action", "adventure", "age", "air", "animal", "beauty", "belief", "birthday", "chance", "change"
]

user_guess_states = {}


def shuffle_word(word):
    """Перемешивает буквы в слове"""
    word = list(word)
    random.shuffle(word)
    return ''.join(word)


def start_guess_word(bot, call):
    """Начало игры 'Угадай слово'"""
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    user_id = call.message.chat.id
    original_word = random.choice(WORDS)
    shuffled_word = shuffle_word(original_word)

    # Сохраняем состояние текущей игры для пользователя
    user_guess_states[user_id] = {
        "original_word": original_word,
        "shuffled_word": shuffled_word
    }

    # Создаем кнопку для пропуска слова
    markup = types.InlineKeyboardMarkup()
    skip_button = types.InlineKeyboardButton('Skip', callback_data='skip_word')
    markup.add(skip_button)

    bot.send_message(
        user_id,
        f'🤔 Guess the word: **{shuffled_word}**',
        parse_mode='Markdown',
        reply_markup=markup
    )


def check_guess(bot, message):
    """Проверка пользовательского ответа в игре 'Угадай слово'"""
    user_id = message.chat.id
    user_data = user_guess_states.get(user_id)

    if not user_data:
        bot.send_message(user_id, "😕 No active game. Please start a new game.")
        return

    if message.text.lower() == user_data["original_word"]:
        current_balance = get_balance(user_id) or 0
        update_balance(user_id, current_balance + 100)

        bot.send_message(user_id, f"🎉 Correct! You earned +100 💰!")
        user_guess_states.pop(user_id)  # Удаляем состояние игры для пользователя
    else:
        bot.send_message(user_id, "❌ Wrong answer. Try again!")


def skip_guess_word(bot, call):
    """Пропуск текущего слова в игре 'Угадай слово'"""
    user_id = call.message.chat.id

    if user_id in user_guess_states:
        user_guess_states.pop(user_id)

    bot.send_message(user_id, "🔄 You skipped the word! Let's try another one.")
    start_guess_word(bot, call)



# Данные пользователей для сохранения состояния





