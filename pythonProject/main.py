import telebot
from telebot import types

bot = telebot.TeleBot('6584407780:AAE8G93fffaZUE-tBQoXFXS70DBQejmgLO4')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('Давай начнем', callback_data='after_start'))
	bot.send_message(message.chat.id, 'Привет! Добро пожаловать в бота, который поможет тебе подготовиться к ЕГЭ по истории. '
									  'Здесь ты найдешь задания, которые помогут тебе запомнить нужную информацию, даже если ты не являешься историческим гуру. '
									  'Давай вместе сделаем шаг к успешной сдаче экзамена!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callbback_message(callback):
	if callback.data == 'after_start':
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton('абоба', callback_data='after_start'))
		bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id, reply_markup=markup)


# @bot.edited_message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, "You edited the message")

# @bot.edited_message_handlers(func=lambda y: True)
# def echo_all(message):
# 	bot.reply_to(message, "You edited the message")

bot.infinity_polling()