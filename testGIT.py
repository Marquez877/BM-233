from utils.random_utils import *
from utils.throw_cubes import *
from utils.casino_utils import *
from utils.games_utils import *
from utils.some_name_for_this_func import *
from utils.profile import *
from utils.jobs_utils import *
bot = telebot.TeleBot('7244608311:AAHrlYJnzHwBpTTZ1Js7QG6gBTwDxtmx3Yw')
db_path = 'casino.db'
user_states = {}
back = '🔙 Back'
casino_players = {}
init_trivia_db()
@bot.message_handler(commands=['sqlite3_private_info'])
def show_users(message):
    try:
        # Список авторизованных пользователей
        allowed_users = [894222865]  # Замените chat_id на актуальные

        if message.chat.id not in allowed_users:
            bot.send_message(chat_id=message.chat.id, text="You are not authorized to use this command.")
            return

        # Инициализация соединения с БД
        connection = get_db_connection()
        cursor = connection.cursor()

        # Извлечение пользователей
        cursor.execute('SELECT chat_id, first_name FROM casino_users')
        casino_players = cursor.fetchall()

        if casino_players:  # Если данные найдены
            text = "Saved users:\n"
            for user in casino_players:
                chat_id, first_name = user
                text += f"Chat ID: {chat_id}, Name: {first_name}\n"

                # Разделение сообщения, если длина текста превышает 4096 символов
                if len(text) > 4000:
                    bot.send_message(chat_id=message.chat.id, text=text)
                    text = ""  # Сброс текста

            if text:  # Отправка остатка
                bot.send_message(chat_id=message.chat.id, text=text)
        else:
            bot.send_message(chat_id=message.chat.id, text="No users saved yet.")

    except Exception as e:
        # Обработка ошибок
        bot.send_message(chat_id=message.chat.id, text=f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, message.from_user.first_name)
    chat_id = message.chat.id
    first_name = message.chat.first_name

    # Приветственный текст
    text = (
        f"👋 *Welcome, {first_name}!*\n\n"
        "I'm *MarqBot*, your friendly assistant! 😎\n\n"
        "🌟 Explore games, enjoy random facts, and test your luck at the casino. \n"
        "✨ Let's get started and have some *fun!* 🎉"
    )

    # Пытаемся получить аватарку пользователя
    photos = bot.get_user_profile_photos(chat_id)
    if photos.total_count > 0:
        # Если есть аватарки, берем первую
        avatar_file_id = photos.photos[0][0].file_id
        bot.send_photo(chat_id, avatar_file_id, caption=text,parse_mode="Markdown")
    else:
        # Если аватарки нет — отправляем запасное фото
        with open("media/cat.jpg",
                  "rb") as photo:
            bot.send_photo(chat_id, photo, caption=text,parse_mode="Markdown")

        # Затем отправляется главное меню
    send_menu(chat_id=chat_id,bot=bot)
#GPT part
@bot.callback_query_handler(func=lambda call: call.data == 'gpt')
def gpt1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, "You can use this free Telegram-Bot to ask quetions: @Buddy_GPTbot ")
    send_menu(call.message.chat.id,bot)
@bot.callback_query_handler(func=lambda call: call.data == 'my_profile')
def profile_callback(call):
    from utils.profile import my_profile
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    my_profile(call.message.chat.id)


# Callback для изменения имени
@bot.callback_query_handler(func=lambda call: call.data == 'edit_profile_name')
def edit_profile_name_callback(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    user_states[chat_id] = 'awaiting_name'  # Устанавливаем состояние "ожидание имени"
    bot.send_message(chat_id, "Please, enter your new name:")


# Обработка ввода нового имени пользователя
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_name')
def process_new_name(message):
    chat_id = message.chat.id

    # Проверка текущего состояния пользователя
    if user_states.get(chat_id) != 'awaiting_name':
        bot.send_message(chat_id, "⚠️ Wrong state. Please, try again later.")
        return

    new_name = message.text.strip()  # Удаляем пробелы

    # Проверяем, доступно ли имя
    from utils.profile import name_exists, update_first_name, my_profile
    if name_exists(new_name):
        bot.send_message(chat_id, f" This name *{new_name}* is already taken. Please, choose another one.",
                         parse_mode="Markdown")
        return  # Не очищаем состояние, чтобы пользователь мог попробовать другой вариант

    # Обновляем имя в базе данных
    update_first_name(chat_id, new_name)
    bot.send_message(chat_id, f"*Your name has been successfully updated to* *{new_name}*!", parse_mode="Markdown")

    # Сбрасываем состояние пользователя
    user_states.pop(chat_id, None)

    # Показываем обновленный профиль
    my_profile(chat_id)
# Information Part
@bot.callback_query_handler(func=lambda call: call.data == 'info')
def info1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    info(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'owner')
def about_owner(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = "🧑‍💻 My owner is Marquez - @marquezpht 😎. Write to him if you have any problems with the bot or if you find any errors and help improve it 😊"
    bot.send_message(call.message.chat.id, text)
    info(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'bot owner')
def about_owner(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    text = "This bot is designed to help and entertain people"
    bot.send_message(call.message.chat.id, text)
    info(call.message.chat.id)


# Manas Part
@bot.callback_query_handler(func=lambda call: call.data == 'manas')
def manas1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    manas(call.message.chat.id)


# Games Part
@bot.callback_query_handler(func=lambda call: call.data == 'games') # для того чтобы зайти
def games1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    games(call.message.chat.id)

#Guess Word
@bot.callback_query_handler(func=lambda call: call.data == 'guess_word') # начало игры
def start_new_game(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = call.message.chat.id
    original_word = random.choice(WORDS)
    shuffled_word = shuffle_word(original_word)
    user_states[user_id] = {
        "original_word": original_word,
        "shuffled_word": shuffled_word
    }
    markup = types.InlineKeyboardMarkup()
    skip_button = types.InlineKeyboardButton('Skip', callback_data='skip_word')
    markup.add(skip_button)
    bot.send_message(user_id, f'Guess the word: **{shuffled_word}**', parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_states) # проверка правильности
def check_guess(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    user_id = message.chat.id
    user_data = user_states.get(user_id)

    if message.text.lower() == user_data["original_word"]:
        current_balance = get_balance(user_id)
        update_balance(user_id, current_balance + 100)
        bot.send_message(user_id, "Correct! 🎉 Great job! You got +100 💰")

        # Убираем состояние игрока
        user_states.pop(user_id)

        # Предлагаем начать новую игру
        markup = types.InlineKeyboardMarkup()
        play_again = types.InlineKeyboardButton('Play Again', callback_data='guess_word')
        back_button = types.InlineKeyboardButton(back, callback_data='back')
        markup.row(play_again)
        markup.row(back_button)
        bot.send_message(user_id, "Want to play again?", reply_markup=markup)
    else:
        bot.send_message(user_id, "Wrong answer. Try again!")

@bot.callback_query_handler(func=lambda call: call.data == 'skip_word') # пропуск слова
def skip_word(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = call.message.chat.id

    # Проверяем, есть ли активная игра у пользователя
    if user_id in user_states:
        # Получаем слово, которое пользователь пропустил
        original_word = user_states[user_id]["original_word"]

        # Сообщаем правильный ответ
        bot.send_message(user_id, f"You skipped the word. The correct word was: **{original_word}**",
                         parse_mode='Markdown')

        # Убираем состояние пользователя
        user_states.pop(user_id)

        # Предлагаем начать новую игру
        markup = types.InlineKeyboardMarkup()
        play_again = types.InlineKeyboardButton('Play Again', callback_data='guess_word')
        back_button = types.InlineKeyboardButton(back, callback_data='back_games')
        markup.add(play_again)
        markup.row(back_button)
        bot.send_message(user_id, "Want to play again?", reply_markup=markup)
    else:
        # Если игры не было
        bot.send_message(user_id, "No active game found. Start a new game!")

#Mathematicians game
user_data = {}

@bot.callback_query_handler(func=lambda call: call.data == 'math_game')
def start_math_game(call):
    chat_id = call.message.chat.id
    # Инициализация данных для пользователя
    user_data[chat_id] = {
        "score": 0,  # Очки
        "current_question": None,  # Текущий вопрос
        "correct_answer": None  # Правильный ответ
    }
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id, "Welcome to the 'Math Game'! 🔢")
    send_math_question(chat_id)
# Обработка текстового сообщения — проверка ответа пользователя
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_math_answer(message):
    chat_id = message.chat.id
    text = message.text

    # Проверяем, является ли ответ числом
    if not text.lstrip('-').isdigit():
        bot.send_message(chat_id, "Please enter a valid number.")
        bot.send_message(chat_id, "Enter the number as a reply to the question.")
        return

    user_answer = int(text)
    correct_answer = user_data[chat_id]['correct_answer']

    # Проверка правильности ответа
    if user_answer == correct_answer:
        user_data[chat_id]['score'] += 1
        current_balance = get_balance(chat_id)
        new_balance = current_balance + 50
        update_balance(chat_id, new_balance)
        update_intelligence_points(chat_id, 1)
        bot.send_message(chat_id, "CONGRATULATIONS! You got it right! 🎉 +50 💰& +1 🧠!")
    else:
        bot.send_message(chat_id, f"Wrong answer 😞. The answer correct is: {correct_answer}")

    # Предложение продолжить игру или вернуться в меню игр
    markup = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton("Continue 🔄", callback_data='continue_math_game')
    back_to_games = types.InlineKeyboardButton("BACK 🔙", callback_data='back_games')
    markup.row(continue_button, back_to_games)
    bot.send_message(chat_id, "Choose what will you do next:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'continue_math_game')
def continue_math_game1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    send_math_question(call.message.chat.id)

def send_math_question(chat_id):
    # Генерация вопроса
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    operator = random.choice(['+', '-'])

    question = f"{num1} {operator} {num2}"
    correct_answer = eval(question)  # Вычисляем правильный ответ

    # Сохраняем текущий вопрос и ответ в памяти пользователя
    user_data[chat_id]['current_question'] = question
    user_data[chat_id]['correct_answer'] = correct_answer

    # Отправляем вопрос
    bot.send_message(chat_id, f"Solve this one: {question}")

@bot.callback_query_handler(func=lambda call: call.data == 'back_games')
def back_games1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    games(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "trivia_challenge")
def start_game(call):
    start_trivia_game(bot, call)


@bot.callback_query_handler(func=lambda call: call.data in ["trivia_true", "trivia_false"])
def process_answer(call):
    user_answer = "True" if call.data == "trivia_true" else "False"
    handle_trivia_answer(bot, call, user_answer)

#Random Things Part
@bot.callback_query_handler(func=lambda call: call.data == 'random_play')
def random_play1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    random_things(call.message.chat.id)
@bot.callback_query_handler(func=lambda call: call.data == 'random_fact')
def random_fact1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    fact = get_random_fact()
    bot.send_message(call.message.chat.id, f"🧠 Random Fact: {fact}")
    random_things(call.message.chat.id)
@bot.callback_query_handler(func=lambda call: call.data == 'random_motivation')
def random_motivation1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    motivation = get_random_motivation()
    bot.send_message(call.message.chat.id, f"💪 Random Motivation: {motivation}")
    random_things(call.message.chat.id)
@bot.callback_query_handler(func=lambda call: call.data == 'random_photo')
def random_photo1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    photo = get_random_photo()
    bot.send_photo(call.message.chat.id, photo)
    random_things(call.message.chat.id)
@bot.callback_query_handler(func=lambda call: call.data == 'random_joke')
def random_joke1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    joke = get_random_joke()
    bot.send_message(call.message.chat.id, f"😂 Random Joke: {joke}")
    random_things(call.message.chat.id)



# Handle Callbacks
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == 'casino':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        casino_menu(bot, call.message.chat.id)  # Добавляем bot
    elif call.data == 'roulette':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        roulette_menu(bot, call.message.chat.id)  # Добавляем bot
    elif call.data == 'rules':  # Show rules
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        rules_menu(call.message.chat.id)  # Добавляем bot
    elif call.data == 'category_number':  # Ставка на число
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "🎯 Enter the number you want to bet on (0-36):")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, lambda m: handle_number_bet(m, bot))  # bot не нужен
    elif call.data == 'throw_cubes':  # Throw Cubes game
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "💰 Enter your bet amount:")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_throw_cubes_bet)

    elif call.data.startswith('category_'):
        category = call.data.split('_')[1]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bet_menu(call.message.chat.id, category)

    elif call.data.startswith('bet_'):
        try:
            _, bet_amount, category = call.data.split('_')
            bet_amount = int(bet_amount)
        except ValueError:
            bot.send_message(call.message.chat.id, "❌ Invalid bet parameters. Try again.")
            return

        current_balance = get_balance(call.message.chat.id)

        # Проверка баланса
        if current_balance is None:
            bot.send_message(call.message.chat.id, "❌ Error: Unable to fetch your balance. Please try again later.")
            return
        if bet_amount <= 0:
            bot.send_message(call.message.chat.id, "❌ Bet amount must be greater than zero.")
            return
        if bet_amount > current_balance:
            bot.send_message(
                call.message.chat.id,
                f"❌ Insufficient funds for the bet! Balance: {current_balance} 💰. Try again."
            )
            bet_menu(call.message.chat.id, category)
            return

        # Проверим возврат функции play_roulette
        result = play_roulette(call.message.chat.id, bet_amount, category)

        if result is None or not isinstance(result, tuple) or len(result) != 2:
            bot.send_message(
                call.message.chat.id,
                "❌ An error occurred while processing your bet. Please try again."
            )
            bet_menu(call.message.chat.id, category)
            return

        # Распакуем результат
        result_message, new_balance = result

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Play Again ⏎', callback_data=f'roulette'),
            types.InlineKeyboardButton('Back to Table 🔙', callback_data='casino')
        )
        bot.send_message(call.message.chat.id, result_message, reply_markup=markup, parse_mode="Markdown")
    elif call.data == 'back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_menu(call.message.chat.id,bot)
    elif call.data == 'back_games':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        games(bot, call.message.chat.id)
    elif call.data == 'forbes':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        show_forbes(call.message.chat.id)
    elif call.data == 'jobs':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        chat_id = call.message.chat.id
        first_name = call.message.chat.first_name

        # Подключаемся к базе данных intellect.db
        connection = sqlite3.connect("intellect.db")
        cursor = connection.cursor()

        # Убедимся, что таблица job_users существует
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE NOT NULL,
                    first_name TEXT
                )
            """)

        # Проверяем, есть ли пользователь в базе
        cursor.execute("SELECT chat_id FROM job_users WHERE chat_id = ?", (chat_id,))
        user_exists = cursor.fetchone()

        if user_exists is None:
            # Если пользователя нет, добавляем
            cursor.execute(
                "INSERT INTO job_users (chat_id, first_name) VALUES (?, ?)",
                (chat_id, first_name)
            )
            connection.commit()
            bot.send_message(chat_id, "✅ You have been successfully added to the Jobs database!")
        else:
            # Если пользователь уже добавлен
            bot.send_message(chat_id, "ℹ️ You are already in the Jobs database!")

        cursor.close()
        connection.close()

        # Показать меню работы
        jobs_menu(chat_id, bot)
    elif call.data == 'loader':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        loader_job(call.message.chat.id, bot)  # Передаем `bot` как аргумент
    elif call.data == 'deliver':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        courier_job(call.message.chat.id, bot)  # Передаем `bot` как аргумент
    elif call.data == 'baker':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        baker_job(call.message.chat.id, bot)  # Передаем `bot` как аргумент
    elif call.data == 'programmer':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        programmer_job_jun(call.message.chat.id, bot)  # Передаем `bot` как аргумент
    elif call.data == 'about_jobs':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        about_jobs(call.message.chat.id,bot)



# Вспомогательные функции



# 1 - GAMES PART FUNCTION

user_states = {}






# Remainder FUNCTIONS
# Функция для отправки напоминаний
def start_periodic_sender():
    sender_thread = threading.Thread(target=send_periodic_messages, daemon=True)
    sender_thread.start()
def send_periodic_messages():
    """
    Отправляет уведомление через bot.send_message всем зарегистрированным пользователям.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT chat_id FROM casino_users')
        chat_ids = cursor.fetchall()  # Получаем список chat_id

        for chat_id in chat_ids:
            try:
                bot.send_message(
                    chat_id[0],
                    "The issues have been resolved. The bot is now fully operational ✅\n\n"
                    "by marquez",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error sending update to chat_id {chat_id[0]}: {e}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


# отправка бесконечных сообщений с периодом времени
# if __name__ == '__main__':
#     init_db()  # Убедимся, что база и таблица созданы
#     start_periodic_sender()



# Запуск бота


# Initialize database and start polling
init_db()
init_trivia_db()
bot.polling(non_stop=True)
