import sqlite3
import re
import datetime
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


@bot.callback_query_handler(func=lambda x: True)
def callback_message(callback):
    if callback.data == "register":
        message = bot.send_message(callback.message.chat.id, f"Вас понял\n"
                                                             f"Укажите Вашу дату рождения в формате дд-мм-гггг\n"
                                                             f"Например, 01-01-2007")

        bot.register_next_step_handler(message, birthdate_handler)


def check(birthdate: str) -> bool:
    try:
        datetime.strptime(birthdate, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def birthdate_handler(birthdate):
    is_valid = check(birthdate.text)
    if is_valid:
        delta_days = (datetime.today().date() - datetime.strptime("21-11-2007", "%d-%m-%Y").date()).days
        year = birthdate.text.split("-")[-1]

        answer_message = (f"Отлично!"
                          f"Вы существуете уже {delta_days} дней!\n\n"
                          f"Помните, что, если вы ошиблись в дате, то всегда можете её изменить, вписав /edit\n"
                          f"Полный список команд: /help")

        # list_of_potential_answers = {"Existence": f"Вы существуете уже {delta_days} дней!\n"}
        #
        # answer_message += list_of_potential_answers["Existence"]
        bot.send_message(birthdate.chat.id, answer_message)
    else:
        bot.send_audio(birthdate.chat.id, open("data/abc.mp3", "rb"), reply_to_message_id=birthdate.message_id)



bot.polling(non_stop=True)
