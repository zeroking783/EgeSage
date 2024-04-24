import telebot
from telebot import types
import psycopg2
from connect import *




bot = telebot.TeleBot('6584407780:AAE8G93fffaZUE-tBQoXFXS70DBQejmgLO4')

@bot.message_handler(commands=['start'])
def send_welcome(message):

	# Здесь я сохраняю name пользователя и id
	user_id = message.from_user.id
	user_name = message.from_user.username

	connection = None
	try:
		# Здесь я подключаюсь к базе данных
		config = load_config()
		connection = psycopg2.connect(**config)
		with connection.cursor() as cursor:
			cursor.execute(
				"INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, user_name)
			)
	except Exception as _ex:
		print("[INFO] ERROR: ", _ex)
	finally:
		if connection is not None:
			connection.close()
			print("[INFO] PostgreSQL connection closed")

	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('Давай начнем', callback_data='after_start'))
	bot.send_message(message.chat.id, 'Привет! Добро пожаловать в бота, который поможет тебе подготовиться к ЕГЭ по истории. '
									  'Здесь ты найдешь задания, которые помогут тебе запомнить нужную информацию, даже если ты не являешься историческим гуру. '
									  'Давай вместе сделаем шаг к успешной сдаче экзамена!', reply_markup=markup)

#
# @bot.callback_query_handler(func=lambda callback: True)
# def callbback_message(callback):
# 	if callback.data == 'after_start':
# 		markup = types.InlineKeyboardMarkup()
# 		markup.add(types.InlineKeyboardButton('абоба', callback_data='after_start'))
# 		bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id, reply_markup=markup)

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#
# 	bot.send_message(message.chat.id, f'Hello {user_name}! Your ID is {user_id}')


# @bot.edited_message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, "You edited the message")

# @bot.edited_message_handlers(func=lambda y: True)
# def echo_all(message):
# 	bot.reply_to(message, "You edited the message")

bot.infinity_polling()