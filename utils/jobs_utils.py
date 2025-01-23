import time
import random
from pyexpat.errors import messages
from .menu_handlers import *
from database_utils import *
from telebot import types
from bot_config import bot


def jobs_menu(chat_id, bot):
    # Получение интеллекта и баланса пользователя


    current_balance = get_balance(chat_id)
    user_intelligence = get_intelligence_points_by_chat_id(chat_id)

    text = (
        "🔍 **Choose your job:**\n\n"
        f"💰 **Your balance:** **{current_balance}** 💼\n"
        f"🧠 **Your intelligence:** **{user_intelligence}**\n\n"
        "Pick a job to start earning! 🛠️ Or learn more by clicking 'ℹ️ About Jobs'."
    )

    # Создание кнопок для меню
    markup = types.InlineKeyboardMarkup()
    loader = types.InlineKeyboardButton("🔧 Loader", callback_data="loader")
    deliver = types.InlineKeyboardButton("🚴 Courier", callback_data="deliver")
    baker = types.InlineKeyboardButton("🍞 Baker", callback_data="baker")
    teacher_job = types.InlineKeyboardButton('👨‍🏫 Teacher', callback_data='teacher_job')
    lawyer_job = types.InlineKeyboardButton('👨‍💼 Lawyer',callback_data='lawyer_job')
    programmer_jun = types.InlineKeyboardButton("💻 Programmer", callback_data="programmer")
    about_jobs = types.InlineKeyboardButton("ℹ️ About Jobs", callback_data="about_jobs")
    back = types.InlineKeyboardButton("🔙 Back", callback_data="back")

    markup.row(loader,deliver)
    markup.row(baker,teacher_job)
    markup.row(lawyer_job,programmer_jun)
    markup.row(about_jobs)
    markup.row(back)

    # Отправка сообщения с меню
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


def about_jobs(chat_id, bot):
    """Информация о работах"""
    text = (
        "ℹ️ **About Jobs:**\n\n"
        "Here is the information about all available jobs:\n\n"
        "🔧 **Loader**:\n"
        "Earn: **200-300 💰**\n"
        "No special requirements are needed. Just move some cargo!\n\n"
        "🚴 **Courier**:\n"
        "Earn: **100-200 💰**\n"
        "No special requirements are needed. Deliver packages around the city.\n\n"
        "🍞 **Baker**:\n"
        "Earn: **400-500 💰**\n"
        "No special requirements. Bake bread, pack it, and you're done!\n\n"
        "💻 **Programmer**:\n"
        "Earn: **1000-2000 💰**\n"
        "🧠 Required intelligence: **50+**\n"
        "Write and debug code, test and publish. Highly paid, but requires more skills.\n\n"
        "Choose your path and start earning! 🛠️"
    )

    # Добавляем кнопку возврата в меню
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("🔙 Back to Jobs", callback_data="back")
    markup.row(back)

    # Отправляем сообщение
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

def about_jobs(chat_id, bot):
    """Информация о работах"""
    text = (
        "ℹ️ **About Jobs:**\n\n"
        "Here is the information about all available jobs:\n\n"
        "🔧 **Loader**:\n"
        "Earn: **200-300 💰**\n"
        "No special requirements are needed. Just move some cargo!\n\n"
        "🚴 **Courier**:\n"
        "Earn: **100-200 💰**\n"
        "No special requirements are needed. Deliver packages around the city.\n\n"
        "🍞 **Baker**:\n"
        "Earn: **400-500 💰**\n"
        "No special requirements. Bake bread, pack it, and you're done!\n\n"
        "💻 **Programmer**:\n"
        "Earn: **1000-2000 💰**\n"
        "🧠 Required intelligence: **50+**\n"
        "Write and debug code, test and publish. Highly paid, but requires more skills.\n\n"
        "Choose your path and start earning! 🛠️"
    )

    # Добавляем кнопку возврата в меню
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("🔙 Back to Jobs", callback_data="back")
    markup.row(back)

    # Отправляем сообщение
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

def loader_job(chat_id, bot):
    message = bot.send_message(chat_id, "🛠️ **You started working as a loader...**")
    time.sleep(1)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📦 Opening the warehouse...")
    time.sleep(1)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🔨 Moving the cargo...")
    time.sleep(1)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🔒 Closing the warehouse...")
    time.sleep(1)

    earnings = random.randint(200, 400)
    current_balance = get_balance(chat_id)
    new_balance = current_balance + earnings
    update_balance(chat_id, new_balance)

    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
        f"🎉 **Job completed!**\n\n"
        f"You earned: **+{earnings}** 💰\n\n"
        f"📊 **Your new balance:** **{new_balance}** 💼"
    ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)


def courier_job(chat_id, bot):
    message = bot.send_message(chat_id, "🚴 **You started working as a courier...**")
    time.sleep(0.5)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📬 Picking up the package...")
    time.sleep(0.5)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🚴 Delivering the package...")
    time.sleep(0.5)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="✅ Confirming the delivery...")
    time.sleep(0.5)

    earnings = random.randint(100, 200)
    current_balance = get_balance(chat_id)
    new_balance = current_balance + earnings
    update_balance(chat_id, new_balance)

    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
        f"🎉 **Job completed!**\n\n"
        f"You earned: **+{earnings}** 💰\n\n"
        f"📊 **Your new balance:** **{new_balance}** 💼"
    ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)


def baker_job(chat_id, bot):
    message = bot.send_message(chat_id, "🍞 **You started working as a baker...**")
    time.sleep(1.2)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="👨‍🍳 Preparing the dough...")
    time.sleep(1.2)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🔥 Baking the bread...")
    time.sleep(1.2)
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📦 Packing the bread...")
    time.sleep(1.2)

    earnings = random.randint(400, 500)
    current_balance = get_balance(chat_id)
    new_balance = current_balance + earnings
    update_balance(chat_id, new_balance)

    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
        f"🎉 **Job completed!**\n\n"
        f"You earned: **+{earnings}** 💰\n\n"
        f"📊 **Your new balance:** **{new_balance}** 💼"
    ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)


def programmer_job_jun(chat_id, bot):
    user_intelligence = get_intelligence_points_by_chat_id(chat_id)

    if user_intelligence >= 50:
        message = bot.send_message(chat_id, "💻 **You started working as a programmer...**")
        time.sleep(1.0)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="👨‍💻 Opening the IDE...")
        time.sleep(1.0)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🖥️ Writing some code...")
        time.sleep(1.0)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🔧 Testing and debugging...")
        time.sleep(1.0)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📤 Publishing the changes...")
        time.sleep(1.0)

        earnings = random.randint(1000, 2000)
        current_balance = get_balance(chat_id)
        new_balance = current_balance + earnings
        update_balance(chat_id, new_balance)

        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
            f"🎉 **Job completed!**\n\n"
            f"You earned: **+{earnings}** 💰\n\n"
            f"📊 **Your new balance:** **{new_balance}** 💼"
        ), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, (
            f"⛔ **Unfortunately, you cannot work as a programmer.**\n\n"
            f"Your intelligence level: **{user_intelligence}** 🧠\n"
            f"💡 Required: **50** 🧠.\n\n"
            f"Increase your intelligence and try again!"
        ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)

def lawyer_job(chat_id, bot):
    user_intelligence = get_intelligence_points_by_chat_id(chat_id)

    # Проверяем уровень интеллекта
    if user_intelligence is None:
        user_intelligence = 1  # Устанавливаем значение по умолчанию

    if user_intelligence >= 35:
        message = bot.send_message(chat_id, "⚖️ **You started working as a lawyer...**")
        time.sleep(1)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📚 Reviewing case files...")
        time.sleep(1)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="✍️ Drafting legal documents...")
        time.sleep(1)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🔎 Researching legal precedents...")
        time.sleep(1)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📢 Presenting arguments in court...")
        time.sleep(1)

        earnings = random.randint(800, 1500)
        current_balance = get_balance(chat_id)
        new_balance = current_balance + earnings
        update_balance(chat_id, new_balance)

        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
            f"🎉 **Job completed!**\n\n"
            f"You earned: **+{earnings}** 💰\n\n"
            f"📊 **Your new balance:** **{new_balance}** 💼"
        ), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, (
            f"⛔ **Unfortunately, you cannot work as a lawyer.**\n\n"
            f"Your intelligence level: **{user_intelligence}** 🧠\n"
            f"💡 Required: **35** 🧠.\n\n"
            f"Increase your intelligence and try again!"
        ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)


def teacher_job(chat_id, bot):
    user_intelligence = get_intelligence_points_by_chat_id(chat_id)

    # Проверяем уровень интеллекта
    if user_intelligence is None:
        user_intelligence = 1  # Устанавливаем значение по умолчанию

    if user_intelligence >= 25:
        message = bot.send_message(chat_id, "📚 **You started working as a teacher...**")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📓 Preparing lesson plans...")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="👩‍🏫 Teaching the class...")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="📝 Grading assignments...")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="🎓 Conducting final reviews...")
        time.sleep(0.8)

        earnings = random.randint(800, 1200)
        current_balance = get_balance(chat_id)
        new_balance = current_balance + earnings
        update_balance(chat_id, new_balance)

        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=(
            f"🎉 **Job completed!**\n\n"
            f"You earned: **+{earnings}** 💰\n\n"
            f"📊 **Your new balance:** **{new_balance}** 💼"
        ), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, (
            f"⛔ **Unfortunately, you cannot work as a teacher.**\n\n"
            f"Your intelligence level: **{user_intelligence}** 🧠\n"
            f"💡 Required: **25** 🧠.\n\n"
            f"Increase your intelligence and try again!"
        ), parse_mode="Markdown")

    jobs_menu(chat_id, bot)


