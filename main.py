import telebot.custom_filters

from handlers import register_handlers
from init_bot import bot

if __name__ == '__main__':
    register_handlers()
    bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
    print("Бот запущен")
    bot.infinity_polling()
