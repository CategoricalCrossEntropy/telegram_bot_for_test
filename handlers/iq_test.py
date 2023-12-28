import telebot.types
from telebot.handler_backends import StatesGroup, State

from init_bot import bot


class Questions(StatesGroup):
    question1 = State()


@bot.message_handler(commands=["iq_test"])
def iq_test(message: telebot.types.Message):
    bot.set_state(message.from_user.id, Questions.question1, message.chat.id)
    bot.send_message(message.chat.id, "Какая высота у Эйфелевой башни? (Укажите значение в метрах)")


@bot.message_handler(state=Questions.question1, func=lambda message: message.text.isdigit())
def correct_height(message: telebot.types.Message):
    difference = abs(312 - int(message.text))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if difference < 15:
            data["iq"] = 80
        elif difference < 60:
            data["iq"] = 40
        else:
            data["iq"] = 15

    text = "Какая самая близкая к Солнцу планета?"
    markup = telebot.util.quick_markup({
        "Юпитер": {"callback_data": "incorrect"},
        "Меркурий": {"callback_data": "correct"},
    })
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(state=Questions.question1)
def incorrect_height(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Необходимо ввести число!")


@bot.callback_query_handler(func=lambda callback: callback.data == "correct")
def correct_planet(callback: telebot.types.CallbackQuery):
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data["iq"] += 80
    bot.send_message(callback.message.chat.id, "Правильно!")
    results(callback)


@bot.callback_query_handler(func=lambda callback: callback.data == "incorrect")
def incorrect_planet(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.message.chat.id, "Неверно(")
    results(callback)


def results(callback: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        iq = data["iq"]
    bot.send_message(callback.message.chat.id, f"Ваш IQ: {iq}")
    bot.delete_state(callback.message.from_user.id, callback.message.chat.id)
