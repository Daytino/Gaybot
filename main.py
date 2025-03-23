import sqlite3
from telebot import *

bot_token = "7781371819:AAFnM-oJZd0GUcTRyZexuMMteN98OsH7mEI"

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["s"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    new_user_button = types.InlineKeyboardButton("Зарегистрировать меня", callback_data="register")
    markup.add(new_user_button)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}\n"
                                      f"Меня зовут <b>Gaybot</b>. Я буду записывать ваши даты дней рождения "
                                      f"и напоминать о них людям в чате",
                     parse_mode="HTML",
                     disable_notification=True,
                     reply_markup=markup)


@bot.message_handler()
def ask(message):
    pass

@bot.callback_query_handler(func=lambda x: True)
def callback_message(callback):
    if callback.data == "register":
        ask()

        bot.send_message(callback.message.chat.id, f"Вас понял\n"
                                                   f"Укажите Вашу дату рождения в формате дд-мм-гггг")
    bot.register_next_step_handler(callback, check)

# поменял
def check(message):
    print(message)

bot.polling(non_stop=True)
