import random
from telebot import types
from database_utils import *
import sqlite3
import requests
from telebot import types
from bot_config import bot

WORDS = [
    "ability", "action", "adventure", "age", "air", "animal", "answer", "area", "army", "art",
    "baby", "back", "ball", "bank", "bed", "bird", "boat", "book", "bottle", "box",
    "boy", "bridge", "brother", "building", "business", "cake", "camera", "car", "cat", "chance",
    "change", "child", "city", "class", "climate", "cloud", "club", "coat", "coffee", "college",
    "color", "company", "computer", "country", "cow", "dance", "day", "deal", "decision", "desk",
    "development", "door", "dream", "drink", "driver", "earth", "education", "effect", "egg", "end",
    "energy", "engine", "event", "example", "experience", "eye", "family", "farm", "father", "field",
    "film", "fire", "fish", "flower", "food", "forest", "friend", "game", "garden", "girl",
    "glass", "goal", "group", "growth", "guide", "hair", "hand", "hat", "health", "heart",
    "history", "holiday", "home", "horse", "hospital", "house", "idea", "industry", "information", "island"
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
        update_intelligence_points(user_id, 2)
        bot.send_message(user_id, f"🎉 Correct! You earned +100 💰& +2 🧠!")
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

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=boolean"


# Состояния пользователей
user_trivia_states = {}
user_guess_states = {}




# === Игровая логика === #
import html  # Модуль для работы с HTML-символами
import time

def fetch_trivia_question():
    """Получение случайного вопроса из Open Trivia DB API"""
    TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=boolean"

    try:
        response = requests.get(TRIVIA_API_URL)

        if response.status_code == 429:  # Слишком много запросов
            print("Превышен лимит запросов. Подождем немного...")
            time.sleep(5)  # Ждем 5 секунд
            return fetch_trivia_question()

        if response.status_code != 200:  # Проверяем остальные коды ответа
            print(f"Ошибка: API вернул код состояния {response.status_code}")
            return None, None

        data = response.json()
        if data["response_code"] == 0 and "results" in data and len(data["results"]) > 0:
            question_data = data["results"][0]
            question = html.unescape(question_data["question"])
            correct_answer = question_data["correct_answer"]
            return question, correct_answer

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса к API: {e}")
        return None, None


def start_trivia_game(bot, call):
    """Начало игры Trivia Challenge"""
    user_id = call.message.chat.id  # Это chat_id пользователя
    user_name = call.message.chat.first_name  # Это имя пользователя, отображаемое в Telegram

    # Удаляем сообщение
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

    # Добавляем пользователя в базу данных
    add_player_to_db(user_id, user_name)  # Исправлено: передаем два аргумента

    # Получаем первый вопрос
    question, correct_answer = fetch_trivia_question()
    if not question:
        bot.send_message(user_id, "❌ Failed to fetch a question. Please try again later.")
        return

    # Сохраняем состояние пользователя
    user_trivia_states[user_id] = {
        "current_question": question,
        "correct_answer": correct_answer
    }

    # Отправка первого вопроса
    markup = types.InlineKeyboardMarkup()
    true_button = types.InlineKeyboardButton("True ✅", callback_data="trivia_true")
    false_button = types.InlineKeyboardButton("False ❌", callback_data="trivia_false")
    back_button = types.InlineKeyboardButton("🔙 Back", callback_data="back_games")
    markup.row(true_button, false_button)
    markup.row(back_button)

    bot.send_message(user_id, f"🎮 Welcome to Trivia Challenge!\n\n🧠 Question: {question}", reply_markup=markup)



def handle_trivia_answer(bot, call, user_answer):
    """Обработка ответа пользователя на вопрос"""
    user_id = call.message.chat.id
    user_name = call.message.chat.first_name
    state = user_trivia_states.get(user_id)

    if not state:
        bot.send_message(user_id, "❌ No active game. Please start a new game.")
        return

    correct_answer = state["correct_answer"]

    # Удаляем предыдущее сообщение
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

    if user_answer == correct_answer:
        # Начисление баланса и очков интеллекта
        current_balance = get_balance(user_id)
        update_balance(user_id, current_balance + 50)  # Использовать user_id
        update_intelligence_points(user_id, 1)  # Здесь заменено user_name на user_id
        bot.send_message(user_id, f"🎉 Correct! You earned +50 💰 and +1 🧠!")
    else:
        bot.send_message(user_id, f"❌ Wrong! The correct answer was: {correct_answer}")

    # Получаем следующий вопрос
    question, correct_answer = fetch_trivia_question()
    if not question:
        bot.send_message(user_id, "❌ Failed to fetch a question. Please try again later.")
        user_trivia_states.pop(user_id, None)
        return

    # Обновляем состояние пользователя
    user_trivia_states[user_id] = {
        "current_question": question,
        "correct_answer": correct_answer
    }

    # Отправляем следующий вопрос
    markup = types.InlineKeyboardMarkup()
    true_button = types.InlineKeyboardButton("True ✅", callback_data="trivia_true")
    false_button = types.InlineKeyboardButton("False ❌", callback_data="trivia_false")
    back_button = types.InlineKeyboardButton("🔙 Back", callback_data="back_games")
    markup.row(true_button, false_button)
    markup.row(back_button)

    bot.send_message(user_id, f"🧠 Next Question: {question}", reply_markup=markup)



