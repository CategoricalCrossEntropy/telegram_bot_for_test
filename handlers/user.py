import telebot

from init_bot import bot


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет! Это бот для прохождения теста!\n\n/iq_test - пройти тестирование")
