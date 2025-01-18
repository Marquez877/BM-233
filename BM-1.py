from operator import truediv

import telebot
import random
import sqlite3
from telebot import types, callback_data
import time
import requests
import threading
bot = telebot.TeleBot('7817287849:AAFxsBwLHgpn22V6I7KK_abplD93T_sKrho')
db_path = 'casino.db'

back = '🔙 Back'
casino_players = {}

# Initialize database
def init_db():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casino_users (
            chat_id INTEGER PRIMARY KEY,
            first_name TEXT,
            balance INTEGER DEFAULT 1000
        )
    ''')
    connection.commit()
    connection.close()
def get_db_connection():
    return sqlite3.connect('casino.db')
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


# Add user to the database
def add_user(chat_id, first_name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM casino_users WHERE chat_id = ?', (chat_id,))
        user = cursor.fetchone()
        if not user:
            cursor.execute(
                'INSERT INTO casino_users (chat_id, first_name, balance) VALUES (?, ?, ?)',
                (chat_id, first_name, 1000)
            )
            connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        connection.close()

def get_all_chat_ids():
    try:
        # Установление соединения и выборка chat_id
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT chat_id FROM casino_users')
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
# Main Menu
def send_menu(chat_id):
    text = f"Choose an option 📲. We have everything to make you happy!"
    casino_players[chat_id] = chat_id
    markup = types.InlineKeyboardMarkup()

    info = types.InlineKeyboardButton('INFO 📋', callback_data='info')
    manas = types.InlineKeyboardButton('MANAS 🎓', callback_data='manas')
    games = types.InlineKeyboardButton('GAMES 👾', callback_data='games')
    random_things = types.InlineKeyboardButton('RANDOM THINGS 🎲', callback_data='random_play')
    gtp_button = types.InlineKeyboardButton('Free Chat GPT ⚪', callback_data='gpt')
    forbes = types.InlineKeyboardButton('FORBES 💸', callback_data='forbes')
    markup.row(info, manas)
    markup.row(games, random_things)
    markup.row(gtp_button)
    casino = types.InlineKeyboardButton('CASINO 🎰', callback_data='casino')
    markup.row(casino)
    markup.row(forbes)
    bot.send_message(chat_id, text, reply_markup=markup)
def info(chat_id):
    text = "What information are you looking for?"
    markup = telebot.types.InlineKeyboardMarkup()
    owner = types.InlineKeyboardButton('About Owner', callback_data='owner')
    bot1 = types.InlineKeyboardButton('About Bot', callback_data='bot owner')
    back_to_main = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(owner,bot1)
    markup.row(back_to_main)
    bot.send_message(chat_id, text, reply_markup=markup)
def manas(chat_id):
    text = 'The necessary information about Manas is stored here:'
    markup = types.InlineKeyboardMarkup()
    obis_test = types.InlineKeyboardButton('Obis Test 📋', url='https://obistest.manas.edu.kg/site/login')
    manas_food = types.InlineKeyboardButton('Manas Yemek 🍴', url='https://beslenme.manas.edu.kg/menu')
    time_table_manas = types.InlineKeyboardButton('Time Table 🕒', url='http://timetable.manas.edu.kg/department')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(obis_test,manas_food,time_table_manas)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)
def games(chat_id):
    text = 'These games are available now:'
    markup = types.InlineKeyboardMarkup()
    guess_word = types.InlineKeyboardButton('Guess Word 🔮', callback_data='guess_word')
    math_game = types.InlineKeyboardButton('Math Game 🧠', callback_data='math_game')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(guess_word)
    markup.row(math_game)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)
def random_things(chat_id):
    text = "Choose what random thing you'd like to see 🎲:"
    markup = types.InlineKeyboardMarkup()
    fact = types.InlineKeyboardButton('Random Fact 🧠', callback_data='random_fact')
    motivation = types.InlineKeyboardButton('Random Motivation 💡', callback_data='random_motivation')
    random_photo = types.InlineKeyboardButton('Random Photo 🏞', callback_data='random_photo')
    joke= types.InlineKeyboardButton('Random Joke 😂', callback_data='random_joke')
    back1 = types.InlineKeyboardButton(back, callback_data='back')
    markup.row(fact, motivation)
    markup.row(random_photo, joke)
    markup.row(back1)
    bot.send_message(chat_id, text, reply_markup=markup)







#CASINO !!!!


# Get user balance
def get_balance(chat_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM casino_users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return None


# Update user balance
def update_balance(chat_id, new_balance):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('UPDATE casino_users SET balance = ? WHERE chat_id = ?', (new_balance, chat_id))
    connection.commit()
    connection.close()





# Casino Menu
def casino_menu(chat_id):
    # Получаем баланс пользователя
    current_balance = get_balance(chat_id)

    if current_balance is None:
        current_balance = 0  # Если баланс не найден, установить значение по умолчанию

    # Обновляем текст с отображением баланса
    text = f'We always make you happy with games! 😊\nYour current balance: {current_balance}💰\nChoose a game you want to play:'

    # Создаем клавиатуру (меню)
    markup = types.InlineKeyboardMarkup()
    roul_button = types.InlineKeyboardButton('ROULETTE 🎡', callback_data='roulette')
    throw_cubes_button = types.InlineKeyboardButton('THROW CUBES 🎲', callback_data='throw_cubes')
    rules = types.InlineKeyboardButton('RULES 📃', callback_data='rules')
    back_button = types.InlineKeyboardButton(back, callback_data='back')

    # Составляем ряд кнопок
    markup.row(roul_button, throw_cubes_button)
    markup.row(rules)
    markup.row(back_button)

    # Отправляем сообщение с фото и клавиатурой
    try:
        with open('welcome_casino.jpg', 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)
    except FileNotFoundError:
        bot.send_message(chat_id, "❌ Image file 'welcome_casino.jpg' not found.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ An error occurred while sending photo: {str(e)}")

def rules_menu(chat_id):
    text = (
        "🎰 *Casino Rules:*\n\n"
        "🎯 *Roulette*: \n"
        "1️⃣ Select a bet category (e.g. '1st 12', 'EVEN', 'RED').\n"
        "2️⃣ Wait for the roulette to show the result.\n"
        "3️⃣ If you win, the reward is bet amount × multiplier.\n\n"
        "🎲 *Throw Cubes*: \n"
        "1️⃣ Choose your bet amount.\n"
        "2️⃣ The player rolls the dice (result: 2 to 12).\n"
        "3️⃣ The bot rolls its dice. If your result is higher, you win your bet.\n"
        "4️⃣ If the bot wins, the bet amount is deducted from your balance.\n\n"
        "Good luck and have fun! 😊"
    )
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("🔙 Back to Casino Menu", callback_data='casino')
    markup.row(back_button)
    bot.send_message(chat_id, text, reply_markup=markup)

# Roulette Game Menu
def roulette_menu(chat_id):
    text = 'Wish good luck 🍀! Choose a category to bet on:'
    markup = types.InlineKeyboardMarkup()

    # Первый ряд
    markup.row(
        types.InlineKeyboardButton('1st 12', callback_data='category_1st'),
        types.InlineKeyboardButton('2nd 12', callback_data='category_2nd'),
        types.InlineKeyboardButton('3rd 12', callback_data='category_3rd')
    )

    # Второй ряд
    markup.row(
        types.InlineKeyboardButton('1 to 18', callback_data='category_1-18'),
        types.InlineKeyboardButton('EVEN', callback_data='category_even'),
        types.InlineKeyboardButton('⚫️', callback_data='category_black'),
        types.InlineKeyboardButton('🔴', callback_data='category_red'),
        types.InlineKeyboardButton('ODD', callback_data='category_odd'),
        types.InlineKeyboardButton('19 to 36', callback_data='category_19-36')
    )
    markup.row(
        types.InlineKeyboardButton('Bet on Number 🎯', callback_data='category_number')
    )

    # Кнопка Back
    back_button = types.InlineKeyboardButton(back, callback_data='casino')
    markup.row(back_button)
    with open('casinoPHOTO.jpg', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)




# Betting Menu
def bet_menu(chat_id, category):
    text = 'How much money 💰do you want to bet?'
    markup = types.InlineKeyboardMarkup()

    # Первый ряд
    markup.row(
        types.InlineKeyboardButton('100 💰', callback_data=f'bet_100_{category}'),
        types.InlineKeyboardButton('500 💰', callback_data=f'bet_500_{category}'),
        types.InlineKeyboardButton('1000 💰', callback_data=f'bet_1000_{category}')
    )

    # Второй ряд
    markup.row(
        types.InlineKeyboardButton('2500 💰', callback_data=f'bet_2500_{category}'),
        types.InlineKeyboardButton('5000 💰', callback_data=f'bet_5000_{category}'),
        types.InlineKeyboardButton('10000 💰', callback_data=f'bet_10000_{category}')
    )

    # Кнопка "Back"
    back_button = types.InlineKeyboardButton(back, callback_data='roulette')
    markup.add(back_button)

    with open('bet-casino.mp4', 'rb') as gif:
        bot.send_animation(chat_id, gif, caption=text, reply_markup=markup)



# Play Roulette


def throw_cubes_game(chat_id, bet_amount):
    # Fetch current balance
    current_balance = get_balance(chat_id)
    if current_balance is None or bet_amount > current_balance:
        markup = types.InlineKeyboardMarkup()
        play_again = types.InlineKeyboardButton('🎮 Play Again', callback_data='throw_cubes')
        back_button = types.InlineKeyboardButton("🔙 Back to Casino Menu", callback_data='casino')
        markup.add(play_again, back_button)
        bot.send_message(
            chat_id,
            "💔 Oops, it seems your balance is too low for this bet. 😞\n"
            "💡 Maybe try a smaller bet or build up your 💰 balance!",
            reply_markup=markup,
            parse_mode="Markdown"
        )

        return

    # Player rolls the dice
    player_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🎲 You roll the dice... You got *{player_roll}*", parse_mode="Markdown")
    time.sleep(2)  # Small delay for effect

    # Bot rolls the dice
    bot_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🤖 Bot rolls the dice... Bot got *{bot_roll}*", parse_mode="Markdown")
    time.sleep(1)

    # Determine the outcome
    markup = types.InlineKeyboardMarkup()
    play_again = types.InlineKeyboardButton('🎮 Play Again', callback_data='throw_cubes')
    back_button = types.InlineKeyboardButton("🔙 Back to Casino Menu", callback_data='casino')
    markup.add(play_again, back_button)

    if player_roll > bot_roll:
        winnings = bet_amount
        new_balance = current_balance + winnings
        update_balance(chat_id, new_balance)
        bot.send_message(
            chat_id,
            f"🎉 *You won!* Your roll: {player_roll}, Bot's roll: {bot_roll}\n"
            f"💰 *Winnings*: {winnings}\n🏆 *New Balance*: {new_balance}",parse_mode="Markdown",reply_markup=markup
        )

    elif player_roll == bot_roll:
        bot.send_message(
            chat_id,
            f"You got the *same* numbers, reroll the dice... Bot got *{bot_roll}* and you got *{player_roll}*... ",
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        new_balance = current_balance - bet_amount
        update_balance(chat_id, new_balance)
        bot.send_message(
            chat_id,
            f"😞 *You lost!* Your roll: {player_roll}, Bot's roll: {bot_roll}\n"
            f"💔 *Lost*: {bet_amount}\n💸 *New Balance*: {new_balance}",parse_mode="Markdown",reply_markup=markup
        )


def play_roulette(chat_id, bet_amount, category):
    """
    Implements the main roulette game logic.
    """
    import random
    import time
    import threading

    try:
        valid_categories = {'1st', '2nd', '3rd', '1-18', '19-36', 'even', 'odd', 'red', 'black'}

        if category not in valid_categories:
            bot.send_message(chat_id, "❌ Invalid category. Please select a valid betting option.")
            return "Invalid category", get_balance(chat_id)

        # Определяем случайный результат рулетки
        roulette_result = random.randint(0, 36)
        current_balance = get_balance(chat_id)

        RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

        won = False
        multiplier = 0

        try:
            with open('roulette-game.mp4', 'rb') as gif:
                animation_msg = bot.send_animation(
                    chat_id, gif,
                    caption='🎡 *The roulette spins...*\nWill luck be on your side? 🤔🍀',
                    parse_mode="Markdown"
                )
            time.sleep(3)
            bot.delete_message(chat_id, animation_msg.message_id)
        except FileNotFoundError:
            bot.send_message(chat_id, "⚠️ Animation file not found. Spinning without animation.")

        # Проверка выигрыша
        if category == '1st' and 1 <= roulette_result <= 12:
            won, multiplier = True, 1.89
        elif category == '2nd' and 13 <= roulette_result <= 24:
            won, multiplier = True, 1.89
        elif category == '3rd' and 25 <= roulette_result <= 36:
            won, multiplier = True, 1.89
        elif category == '1-18' and 1 <= roulette_result <= 18:
            won, multiplier = True, 0.89
        elif category == '19-36' and 19 <= roulette_result <= 36:
            won, multiplier = True, 0.89
        elif category == 'even' and roulette_result != 0 and roulette_result % 2 == 0:
            won, multiplier = True, 0.89
        elif category == 'odd' and roulette_result % 2 == 1:
            won, multiplier = True, 0.89
        elif category == 'red' and roulette_result in RED_NUMBERS:
            won, multiplier = True, 0.89
        elif category == 'black' and roulette_result in BLACK_NUMBERS:
            won, multiplier = True, 0.89

        # Обновление баланса и формирование сообщений
        if won:
            winnings = int(bet_amount * multiplier)
            new_balance = current_balance + winnings
            update_balance(chat_id, new_balance)
            result_text = (
                f"🎉 *The ball stopped on {roulette_result}!* 🥳\n"
                f"💰 You *WIN*: {winnings} coins!\n"
                f"✨ *Congratulations!* Your *new balance*: {new_balance} 💸"
            )
        else:
            new_balance = current_balance - bet_amount
            update_balance(chat_id, new_balance)
            result_text = (
                f"💔 *The ball stopped on {roulette_result}...*\n"
                f"😞 You *lost*: {bet_amount} coins.\n"
                f"💰 Your *current balance*: {new_balance} 💸\n"
                "💡 *Don't give up!* Maybe luck will visit you soon. 🍀",
            )

        return result_text, new_balance

    except Exception as e:
        print(f"Error in play_roulette: {e}")
        bot.send_message(chat_id, "⚠️ An error occurred during the game. Please try again later.")
        return f"Error occurred: {e}", get_balance(chat_id)



def handle_throw_cubes_bet(message):
    try:
        bet_amount = int(message.text)
        if bet_amount <= 0:
            bot.send_message(message.chat.id, "❌ Bet amount must be greater than 0!")
            bot.register_next_step_handler(message, handle_throw_cubes_bet)
            return

        # Start the dice game
        throw_cubes_game(message.chat.id, bet_amount)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please enter a valid number for your bet!")
        bot.register_next_step_handler(message, handle_throw_cubes_bet)

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
        with open("cat.jpg",
                  "rb") as photo:
            bot.send_photo(chat_id, photo, caption=text,parse_mode="Markdown")

        # Затем отправляется главное меню
    send_menu(chat_id=chat_id)
#GPT part
@bot.callback_query_handler(func=lambda call: call.data == 'gpt')
def gpt1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, "You can use this free Telegram-Bot to ask quetions: @Buddy_GPTbot ")
    send_menu(call.message.chat.id)


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
        bot.send_message(user_id, "Correct! 🎉 Great job!")

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
        bot.send_message(chat_id, "Enter the number as a reply to the question.")
        return

    user_answer = int(text)
    correct_answer = user_data[chat_id]['correct_answer']

    # Проверка правильности ответа
    if user_answer == correct_answer:
        user_data[chat_id]['score'] += 1
        bot.send_message(chat_id, "CONGRATULATIONS! You got it right! 🎉")
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
@bot.callback_query_handler(func=lambda call: call.data == 'back_games')
def back_games1(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    games(call.message.chat.id)
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
        casino_menu(call.message.chat.id)
    elif call.data == 'roulette':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        roulette_menu(call.message.chat.id)
    elif call.data == 'rules':  # Show rules
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        rules_menu(call.message.chat.id)
    elif call.data == 'category_number':  # Ставка на число
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "🎯 Enter the number you want to bet on (0-36):")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id,handle_number_bet)# Ожидаем число от пользователя
    elif call.data == 'throw_cubes':  # Throw Cubes game
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "💰 Enter your bet amount:")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_throw_cubes_bet)

    elif call.data.startswith('category_'):
        category = call.data.split('_')[1]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bet_menu(call.message.chat.id, category)

    elif call.data.startswith('bet_'):
        _, bet_amount, category = call.data.split('_')
        bet_amount = int(bet_amount)
        current_balance = get_balance(call.message.chat.id)
        # проверка баланса
        if bet_amount > current_balance:
            bot.send_message(call.message.chat.id,
                             f"❌ У вас недостаточно средств для ставки! Баланс: {current_balance} 💰. Попробуйте снова.")
            bet_menu(call.message.chat.id, category)
            return

            # Проверим возврат функции play_roulette
        result = play_roulette(call.message.chat.id, bet_amount, category)

        # Добавляем диагностику результата



        # Распаковываем безопасно
        result_message, new_balance = result

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Play Again ⏎', callback_data=f'roulette'),
            types.InlineKeyboardButton('Back to Table 🔙', callback_data='casino')
        )
        bot.send_message(call.message.chat.id, result_message, reply_markup=markup,parse_mode="Markdown")
    elif call.data == 'back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_menu(call.message.chat.id)
    elif call.data == 'back_games':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        games(call.message.chat.id)
    elif call.data == 'forbes':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        show_forbes(call.message.chat.id)

def handle_number_bet(message):
    try:
        number = int(message.text)  # Пробуем преобразовать ввод в число
        if not 0 <= number <= 36:  # Проверяем, что число в диапазоне 0-36
            bot.send_message(message.chat.id, "❌ Please enter a valid number between 0 and 36.")
            bot.register_next_step_handler(message, handle_number_bet)
            return

        # Если число валидно, запрашиваем сумму ставки
        bot.send_message(
            message.chat.id, f"You selected number {number} ✨. How much money do you want to bet? 💸"
        )
        bot.register_next_step_handler(
            message, lambda bet_message: process_number_bet(message.chat.id, number, bet_message)
        )
    except ValueError:  # Если пользователь ввел не число
        bot.send_message(message.chat.id, "❌ Please enter a valid number between 0 and 36.")
        bot.register_next_step_handler(message, handle_number_bet)
def process_number_bet(chat_id, number, bet_message):
    try:
        bet_amount = int(bet_message.text)  # Пробуем преобразовать ставку в число
        current_balance = get_balance(chat_id)

        if bet_amount <= 0:
            bot.send_message(chat_id, "❌ Bet amount must be greater than zero.")
            bot.register_next_step_handler(bet_message, lambda bm: process_number_bet(chat_id, number, bm))
            return
        elif bet_amount > current_balance:
            bot.send_message(
                chat_id,
                "😢 *Your balance is insufficient for this bet.*\n💡 Try a smaller wager or earn more coins!",
                parse_mode="Markdown"
            )
            time.sleep(2)
            casino_menu(chat_id)
            bot.register_next_step_handler(bet_message, lambda bm: process_number_bet(chat_id, number, bm))
            return

        # Игровая логика для ставки на число
        result_message, new_balance = play_roulette_number(chat_id, bet_amount, number)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Play Again 🔄', callback_data=f'roulette'),
            types.InlineKeyboardButton('Casino Menu 🎰', callback_data='casino')
        )
        bot.send_message(chat_id, result_message, reply_markup=markup)
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a valid bet amount.")
        bot.register_next_step_handler(bet_message, lambda bm: process_number_bet(chat_id, number, bm))
def play_roulette_number(chat_id, bet_amount, number):
    try:
        roulette_result = random.randint(0, 36)
        current_balance = get_balance(chat_id)

        if current_balance is None or bet_amount <= 0 or bet_amount > current_balance:
            return "Invalid bet: make sure your bet is positive and within your balance.", current_balance
        # Уведомление пользователя о спине рулетки
        with open('roulette-game.mp4', 'rb') as gif:
            animation_msg = bot.send_animation(chat_id, gif, caption='The ball is spinning...')
        time.sleep(4)
        # Удаляем только гифку через 0.1 секунду
        threading.Timer(0.1, lambda: bot.delete_message(chat_id, animation_msg.message_id)).start()

        # Проверка выигрыша
        if roulette_result == number:
            multiplier = 35
            winnings = int(bet_amount * multiplier)
            new_balance = current_balance + winnings
            update_balance(chat_id, new_balance)
            return f"You WON! 🎉 The ball landed on {roulette_result}. Your winnings: {winnings}. New balance: {new_balance}.", new_balance
        else:
            new_balance = current_balance - bet_amount
            update_balance(chat_id, new_balance)
            return f"You LOST. 😢 The ball landed on {roulette_result}. Your new balance: {new_balance}.", new_balance

    except Exception as e:
        print(f"Error in play_roulette_number: {e}")
        return "Internal error occurred. Please try again later.", None
def show_forbes(chat_id):
    """
    Отображает топ-10 богатых пользователей.
    Формат: место, имя, баланс. Медали для 1-3 мест.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Запрашиваем 10 пользователей с наибольшим балансом
        cursor.execute("SELECT first_name, balance FROM casino_users ORDER BY balance DESC LIMIT 10")
        top_users = cursor.fetchall()

        # Если топ пустой
        if not top_users:
            bot.send_message(chat_id, "Forbes list is empty 🙁")
            return

        # Составляем сообщение
        text = "💸 *FORBES Richest Players*\n\n🏆 Here are the wealthiest players daring to challenge luck:\n\n"
        medals = ["🥇", "🥈", "🥉"]  # Медали для первых трёх мест

        for index, (name, balance) in enumerate(top_users, start=1):
            if index <= 3:
                medal = medals[index - 1]  # Присваиваем медаль для 1-3 мест
            else:
                medal = f"{index}⃣"  # Остальные — число с эмодзи
            text += f"{medal} *{index}.* {name} — {balance} 💰\n"

        # Добавляем возможность вернуться в меню
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("🔙 Back", callback_data="back")
        markup.add(back_button)

        # Отправка сообщения
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        # Сообщаем об ошибке
        bot.send_message(chat_id, f"An error occurred: {e}")
        print(f"Error fetching Forbes data: {e}")
    finally:
        cursor.close()
        connection.close()
# Вспомогательные функции

# 1 - GAMES PART FUNCTIONS
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
user_states = {}
def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def send_math_question(chat_id):
    # Генерация вопроса
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, 1000)
    operator = random.choice(['+', '-', '*'])

    question = f"{num1} {operator} {num2}"
    correct_answer = eval(question)  # Вычисляем правильный ответ

    # Сохраняем текущий вопрос и ответ в памяти пользователя
    user_data[chat_id]['current_question'] = question
    user_data[chat_id]['correct_answer'] = correct_answer

    # Отправляем вопрос
    bot.send_message(chat_id, f"Solve this one: {question}")


# 2 - RANDOM THINGS PART FUNCTIONS
def get_random_fact():
    try:
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['text']
        else:
            return "Could not fetch a fact right now."
    except Exception as e:
        print(f"Error fetching fact: {str(e)}")
        return "Error fetching fact."

def get_random_joke():
    try:
        url = 'https://official-joke-api.appspot.com/random_joke'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} - {data['punchline']}"
        else:
            return "Could not fetch a joke right now."
    except Exception as e:
        print(f"Error fetching joke: {str(e)}")
        return "Error fetching joke."

def get_random_photo():
    return f'https://picsum.photos/200/300?random={random.randint(1, 1000)}'

def get_random_motivation():
    try:
        url = 'https://zenquotes.io/api/random'
        response = requests.get(url)
        if response.status_code == 200:
            quotes = response.json()
            random_quote = random.choice(quotes)
            return random_quote['q']
        else:
            return "Could not fetch motivation right now."
    except Exception as e:
        print(f"Error fetching motivation: {str(e)}")
        return f"Error fetching motivation: {str(e)}"

# Remainder FUNCTIONS
# Функция для отправки напоминаний
def start_periodic_sender():
    sender_thread = threading.Thread(target=send_periodic_messages, daemon=True)
    sender_thread.start()
def notify_students(chat_id):
    text = ("Добрый день, студент группы BM-23! Не забудьте зарегистрироваться на предметы через OBIS TEST.\n\n"
            "⏳ Регистрация доступна до **20 января, 17:30**.\n\n"
            "Кутман күн, BM-23 студент! OBIS TEST системасында сабактарга каттоо керектигин унутпаңыз.\n\n"
            "⏳ Каттоо **20-январь саат 17:30га чейин** жеткиликтүү.\n\n"
            "by marquez")
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('🔗 Перейти на OBIS TEST', url='https://obistest.manas.edu.kg/site/login')
    markup.add(button)
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
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
                notify_students(chat_id[0])
            except Exception as e:
                print(f"Error sending update to chat_id {chat_id[0]}: {e}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


# # отправка бесконечных сообщений с периодом времени
# if __name__ == '__main__':
#     init_db()  # Убедимся, что база и таблица созданы
#     start_periodic_sender()



# Запуск бота


# Initialize database and start polling
init_db()
bot.polling(non_stop=True)
