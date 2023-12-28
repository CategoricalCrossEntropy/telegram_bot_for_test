import telebot
from telebot import StateMemoryStorage

from config import TOKEN

bot = telebot.TeleBot(TOKEN, state_storage=StateMemoryStorage())
