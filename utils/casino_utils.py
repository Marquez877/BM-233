
from telebot import types
from database_utils import *
import random
import time
from bot_config import bot
back = '🔙 Back'


def casino_menu(bot, chat_id):
    """Меню казино"""
    current_balance = get_balance(chat_id)

    # Текст с балансом
    text = (f'We always make you happy with games! 😊\n\n'
            f'*Your current balance: {current_balance} 💰\n\n*'
            'Choose a game you want to play:')

    # Меню казино
    markup = types.InlineKeyboardMarkup()
    roul_button = types.InlineKeyboardButton('ROULETTE 🎡', callback_data='roulette')
    throw_cubes_button = types.InlineKeyboardButton('THROW CUBES 🎲', callback_data='throw_cubes')
    rules = types.InlineKeyboardButton('RULES 📃', callback_data='rules')
    back_button = types.InlineKeyboardButton(back, callback_data='back')

    markup.row(roul_button, throw_cubes_button)
    markup.row(rules)
    markup.row(back_button)

    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


def roulette_menu(bot, chat_id):
    """Меню рулетки"""
    text = 'Wish good luck 🍀! Choose a category to bet on:'
    markup = types.InlineKeyboardMarkup()

    # Кнопки категорий ставок
    markup.row(
        types.InlineKeyboardButton('1st 12', callback_data='category_1st'),
        types.InlineKeyboardButton('2nd 12', callback_data='category_2nd'),
        types.InlineKeyboardButton('3rd 12', callback_data='category_3rd')
    )

    markup.row(
        types.InlineKeyboardButton('1 to 18', callback_data='category_1-18'),
        types.InlineKeyboardButton('EVEN', callback_data='category_even'),
        types.InlineKeyboardButton('⚫️', callback_data='category_black'),
        types.InlineKeyboardButton('🔴', callback_data='category_red'),
        types.InlineKeyboardButton('ODD', callback_data='category_odd'),
        types.InlineKeyboardButton('19 to 36', callback_data='category_19-36')
    )
    markup.row(types.InlineKeyboardButton('Bet on Number 🎯', callback_data='category_number'))
    back_button = types.InlineKeyboardButton(back, callback_data='casino')
    markup.row(back_button)
    bot.send_message(chat_id, text, reply_markup=markup)


def play_roulette(chat_id, bet_amount, category):
    """
    Implements the main roulette game logic.
    """
    import random
    import time

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
            with open('../media/roulette-game.mp4', 'rb') as gif:
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

    with open('../media/bet-casino.mp4', 'rb') as gif:
        bot.send_animation(chat_id, gif, caption=text, reply_markup=markup)

import threading
from database_utils import get_balance, update_balance  # Для работы с базой данных


# Логика игры: Ставка на число
def play_roulette_number(chat_id, bet_amount, number, bot):
    """
    Основная логика игры рулетки на числа.
    """
    try:
        roulette_result = random.randint(0, 36)
        current_balance = get_balance(chat_id)

        if current_balance is None or bet_amount <= 0 or bet_amount > current_balance:
            return "Invalid bet: make sure your bet is positive and within your balance.", current_balance

        # Уведомление: вращение рулетки
        with open('../media/roulette-game.mp4', 'rb') as gif:
            animation_msg = bot.send_animation(chat_id, gif, caption='The ball is spinning...')
        time.sleep(4)
        # Удаляем сообщение с гифкой через небольшой интервал времени
        threading.Timer(0.1, lambda: bot.delete_message(chat_id, animation_msg.message_id)).start()

        # Проверяем результат
        if roulette_result == number:
            multiplier = 35
            winnings = int(bet_amount * multiplier)
            new_balance = current_balance + winnings
            update_balance(chat_id, new_balance)
            return (
                f"You WON! 🎉 The ball landed on {roulette_result}. Your winnings: {winnings}. New balance: {new_balance}.",
                new_balance
            )
        else:
            new_balance = current_balance - bet_amount
            update_balance(chat_id, new_balance)
            return (
                f"You LOST. 😢 The ball landed on {roulette_result}. Your new balance: {new_balance}.",
                new_balance
            )

    except Exception as e:
        print(f"Error in play_roulette_number: {e}")
        return "Internal error occurred. Please try again later.", None

import telebot

def process_number_bet(chat_id, number, bet_message, bot):
    """
    Обработка ставки: проверяет сумму ставки, баланс и вызывает игру.
    """
    try:
        bet_amount = int(bet_message.text)
        current_balance = get_balance(chat_id)

        if bet_amount <= 0:
            bot.send_message(chat_id, "❌ Bet amount must be greater than zero.")
            bot.register_next_step_handler(
                bet_message,
                lambda bm: process_number_bet(chat_id, number, bm, bot)
            )
            return
        elif bet_amount > current_balance:
            bot.send_message(
                chat_id,
                "😢 *Your balance is insufficient for this bet.*\n💡 Try a smaller wager or earn more coins!",
                parse_mode="Markdown"
            )
            time.sleep(2)
            return  # Завершаем обработку

        # Игровая логика
        result_message, new_balance = play_roulette_number(chat_id, bet_amount, number, bot)

        # Ответ пользователю
        markup = telebot.types.InlineKeyboardMarkup()  # Исправлено: используем telebot.types
        markup.add(
            telebot.types.InlineKeyboardButton('Play Again 🔄', callback_data=f'roulette'),
            telebot.types.InlineKeyboardButton('Casino Menu 🎰', callback_data='casino'),
        )
        bot.send_message(chat_id, result_message, reply_markup=markup)

    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a valid bet amount.")
        bot.register_next_step_handler(
            bet_message,
            lambda bm: process_number_bet(chat_id, number, bm, bot)
        )

def handle_number_bet(message, bot):
    """
    Обработка ввода числа для ставки.
    """
    try:
        number = int(message.text)  # Пробуем преобразовать ввод в число
        if not 0 <= number <= 36:  # Проверка диапазона
            bot.send_message(message.chat.id, "❌ Please enter a valid number between 0 and 36.")
            bot.register_next_step_handler(message, lambda m: handle_number_bet(m, bot))
            return

        # Если число валидно, запрашиваем сумму ставки
        bot.send_message(
            message.chat.id,
            f"You selected number {number} ✨. How much money do you want to bet? 💸"
        )
        bot.register_next_step_handler(
            message,
            lambda bet_message: process_number_bet(message.chat.id, number, bet_message, bot)
        )

    except ValueError:  # Если пользователь ввел не число
        bot.send_message(message.chat.id, "❌ Please enter a valid number between 0 and 36.")
        bot.register_next_step_handler(message, lambda m: handle_number_bet(m, bot))

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