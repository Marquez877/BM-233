import telebot
import random
import sqlite3
from telebot import types
import time

bot = telebot.TeleBot('')
db_path = 'casino.db'

back = '🔙 Back'


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


# Add user to the database
def add_user(chat_id, first_name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM casino_users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO casino_users (chat_id, first_name, balance) VALUES (?, ?, ?)',
                       (chat_id, first_name, 1000))
        connection.commit()
    connection.close()


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


# Main Menu
def send_menu(chat_id):
    text = 'WELCOME'
    markup = types.InlineKeyboardMarkup()
    casino = types.InlineKeyboardButton('CASINO', callback_data='casino')
    markup.add(casino)
    bot.send_message(chat_id, text, reply_markup=markup)


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
    roul_button = types.InlineKeyboardButton('Roulette', callback_data='roulette')
    throw_cubes_button = types.InlineKeyboardButton('THROW CUBES', callback_data='throw_cubes')
    rules = types.InlineKeyboardButton('RULES', callback_data='rules')
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
        "3️⃣ The bot rolls its dice. If your result is higher, you win 2× your bet.\n"
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
    markup.add(
        types.InlineKeyboardButton('Bet on Number 🎯', callback_data='category_number')
    )

    # Кнопка Back
    back_button = types.InlineKeyboardButton(back, callback_data='casino_menu')
    markup.add(back_button)
    with open('casinoPHOTO.jpg', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)




# Betting Menu
def bet_menu(chat_id, category):
    text = 'How much money ₥ do you want to bet?'
    markup = types.InlineKeyboardMarkup()

    # Первый ряд
    markup.row(
        types.InlineKeyboardButton('1₥', callback_data=f'bet_1_{category}'),
        types.InlineKeyboardButton('10 💰', callback_data=f'bet_10_{category}'),
        types.InlineKeyboardButton('50 💰', callback_data=f'bet_50_{category}')
    )

    # Второй ряд
    markup.row(
        types.InlineKeyboardButton('100 💰', callback_data=f'bet_100_{category}'),
        types.InlineKeyboardButton('500 💰', callback_data=f'bet_500_{category}'),
        types.InlineKeyboardButton('1000 💰', callback_data=f'bet_1000_{category}')
    )

    # Кнопка "Back"
    back_button = types.InlineKeyboardButton(back, callback_data='roulette_menu')
    markup.add(back_button)

    with open('bet-casino.mp4', 'rb') as gif:
        bot.send_animation(chat_id, gif, caption=text, reply_markup=markup)



# Play Roulette


def throw_cubes_game(chat_id, bet_amount):
    # Fetch current balance
    current_balance = get_balance(chat_id)
    if current_balance is None or bet_amount > current_balance:
        bot.send_message(chat_id, "❌ You don't have enough 💰 for this bet!")
        return

    # Player rolls the dice
    player_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🎲 You roll the dice... You got *{player_roll}*", parse_mode="Markdown")
    time.sleep(2)  # Small delay for effect

    # Bot rolls the dice
    bot_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🤖 Bot rolls the dice... It got *{bot_roll}*", parse_mode="Markdown")
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
            f"🎉 You *win*! Your new balance: {new_balance} 💰",
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        new_balance = current_balance - bet_amount
        update_balance(chat_id, new_balance)
        bot.send_message(
            chat_id,
            f"😢 The bot wins! Your new balance: {new_balance} 💰",
            parse_mode="Markdown",
            reply_markup=markup
        )
def play_roulette(chat_id, bet_amount, category):
    """
    Logic of the roulette game.
    """
    roulette_result = random.randint(0, 36)
    current_balance = get_balance(chat_id)

    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    won = False  # Default: lost
    multiplier = 0

    # Notify user about spinning the roulette
    with open('roulette-game.mp4', 'rb') as gif:
        bot.send_animation(chat_id,gif,caption='The ball is spinning...')
        time.sleep(4)  # Задержка на 2 секунды

    # Check winning conditions
    if category == '1st' and 1 <= roulette_result <= 12:
        won, multiplier = True, 2.89
    elif category == '2nd' and 13 <= roulette_result <= 24:
        won, multiplier = True, 2.89
    elif category == '3rd' and 25 <= roulette_result <= 36:
        won, multiplier = True, 2.89
    elif category == '1-18' and 1 <= roulette_result <= 18:
        won, multiplier = True, 1.89
    elif category == '19-36' and 19 <= roulette_result <= 36:
        won, multiplier = True, 1.89
    elif category == 'even' and roulette_result != 0 and roulette_result % 2 == 0:
        won, multiplier = True, 1.89
    elif category == 'odd' and roulette_result % 2 == 1:
        won, multiplier = True, 1.89
    elif category == 'red' and roulette_result in RED_NUMBERS:
        won, multiplier = True, 1.89
    elif category == 'black' and roulette_result in BLACK_NUMBERS:
        won, multiplier = True, 1.89

    # Update balance based on outcome
    if won:
        winnings = int(bet_amount * multiplier)
        new_balance = current_balance + winnings
        update_balance(chat_id, new_balance)
        return f"You WON! 🎉 Result: {roulette_result}. Your new balance: {new_balance}₥", new_balance
    else:
        new_balance = current_balance - bet_amount
        update_balance(chat_id, new_balance)
        return f"You LOST. 😢 Result: {roulette_result}. Your new balance: {new_balance}₥", new_balance
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
    send_menu(chat_id=message.chat.id)


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
        result_message, new_balance = play_roulette(call.message.chat.id, bet_amount, category)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Play Again ⏎', callback_data=f'roulette'),
            types.InlineKeyboardButton('Main Menu 🔙', callback_data='casino')
        )
        bot.send_message(call.message.chat.id, result_message, reply_markup=markup)
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
            bot.send_message(chat_id, "❌ You don't have enough balance for this bet.")
            bot.register_next_step_handler(bet_message, lambda bm: process_number_bet(chat_id, number, bm))
            return

        # Игровая логика для ставки на число
        result_message, new_balance = play_roulette_number(chat_id, bet_amount, number)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Play Again', callback_data=f'roulette'),
            types.InlineKeyboardButton('Main Menu', callback_data='casino')
        )
        bot.send_message(chat_id, result_message, reply_markup=markup)
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a valid bet amount.")
        bot.register_next_step_handler(bet_message, lambda bm: process_number_bet(chat_id, number, bm))
def play_roulette_number(chat_id, bet_amount, number):
    roulette_result = random.randint(0, 36)
    current_balance = get_balance(chat_id)

    # Уведомляем, что рулетка крутится
    with open('roulette-game.mp4', 'rb') as gif:
        bot.send_animation(chat_id, gif, caption='The ball is spinning...')
        time.sleep(4)

    # Проверяем результат игры
    if roulette_result == number:
        multiplier = 35  # Умножение ставки на 35 при выигрыше
        winnings = bet_amount * multiplier
        new_balance = current_balance + winnings
        update_balance(chat_id, new_balance)
        return f"You WON! 🎉 The ball landed on {roulette_result}. Your winnings: {winnings}. New balance: {new_balance}.", new_balance
    else:
        new_balance = current_balance - bet_amount
        update_balance(chat_id, new_balance)
        return f"You LOST. 😢 The ball landed on {roulette_result}. Your new balance: {new_balance}.", new_balance
# Initialize database and start polling
init_db()
bot.polling(non_stop=True)
