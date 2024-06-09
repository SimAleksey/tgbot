
from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import keyboard as kb
from googletrans import Translator, LANGCODES
import database as db


load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = TeleBot(token=TOKEN)
translator = Translator()

# @bot.message_handler(commands=['start', 'help'])
# def start(message: types.Message):
#     chat_id = message.chat.id
#     first_name = message.from_user.first_name
#     if message.text == '/start':
#         bot.send_message(chat_id, f'Привет, {first_name}')
#     elif message.text == '/help':
#         bot.send_message(chat_id, 'Помощь по боту')
#
#
# @bot.message_handler(content_types=['text'])
# def answer(message: types.Message):
#      chat_id = message.chat.id
#      bot.send_message(chat_id, message.text)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    db.add_user(first_name, chat_id)
    bot.send_message(chat_id, 'Выберите действие снизу', reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_translation(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, с которого хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_from)

@bot.message_handler(func=lambda msg: msg.text == 'History')
def history(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, db.history(chat_id))


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, на который хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_tu, message.text)


def get_lang_tu(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message: types.Message, lang_from, lang_tu):
    chat_id = message.chat.id
    _from = LANGCODES[lang_from.lower()]
    _tu = LANGCODES[lang_tu.lower()]
    translator_text = translator.translate(message.text, dest=_tu, src=_from).text
    db.add_translated(message.text, translator_text, _from, _tu, chat_id)
    bot.send_message(chat_id, translator_text)
    start(message)


bot.polling(none_stop=True)
