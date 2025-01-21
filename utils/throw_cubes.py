import random
from telebot import types
from database_utils import get_balance, update_balance
from bot_config import bot
import time
def throw_cubes_game(chat_id, bet_amount):
    """Игра 'Бросок кубиков'"""
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

    player_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🎲 You roll the dice... You got *{player_roll}*", parse_mode="Markdown")
    time.sleep(2)
    bot_roll = random.randint(2, 12)
    bot.send_message(chat_id, f"🤖 Bot rolls the dice... Bot got *{bot_roll}*", parse_mode="Markdown")

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
            f"💰 *Winnings*: {winnings}\n🏆 *New Balance*: {new_balance}",
            parse_mode="Markdown",
            reply_markup=markup
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
            f"💸 *New Balance*: {new_balance}",
            parse_mode="Markdown",
            reply_markup=markup
        )
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