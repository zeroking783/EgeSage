import telebot
from telebot import types
import psycopg2
from connect import *
import datetime
import random

bot = telebot.TeleBot('6584407780:AAE8G93fffaZUE-tBQoXFXS70DBQejmgLO4')

def answer_random(answer_true, answer_fall):
	all_answer = []
	all_answer.append(answer_true)
	for i in range(len(answer_fall)):
		all_answer.append((str(answer_fall[i]))[2:-3])
	random.shuffle(all_answer)
	return all_answer

@bot.message_handler(commands=['start'])
def send_welcome(message):

	# Здесь я сохраняю name пользователя и id
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()
	cursor.execute(
					"INSERT INTO users (user_id, username, user_state) VALUES (%s, %s, %s) ON CONFLICT (user_id)"
							" DO UPDATE SET username = EXCLUDED.username, user_state = EXCLUDED.user_state",
						(message.from_user.id, message.from_user.username, 'start')
					)

	connection.commit()
	cursor.close()
	connection.close()

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn_menu = types.KeyboardButton('Меню')
	markup.row(btn_menu)
	bot.send_message(message.chat.id, 'Привет! Добро пожаловать в бота, который поможет тебе подготовиться к ЕГЭ по истории. '
									  'Здесь ты найдешь задания, которые помогут тебе запомнить нужную информацию, даже если ты не являешься историческим гуру. '
									  'Давай вместе сделаем шаг к успешной сдаче экзамена!', reply_markup=markup)
	bot.delete_message(message.chat.id, message.message_id)

# @bot.message_handler(commands=['Давай начнем'])
# def delete_welcome_message(message):
# 	bot.delete_message(message.chat_id, message.message_id)

@bot.message_handler(content_types=['text'])
def on_click(message):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Получаю состояние юзера
	cursor.execute(f"SELECT user_state FROM users WHERE user_id = {message.from_user.id}")
	user_state = (cursor.fetchone())[0]

	if 'test' in user_state and message.text == 'Меню':
		bot.delete_message(message.chat.id, message.message_id-1)

	if message.text == 'Меню':

		# Переменная с датой пользователя
		current_time = datetime.datetime.now()

		# Обновляем состояние пользователя на
		cursor.execute(f"UPDATE users SET user_state = %s, last_launch = %s, selected_questions = %s, selected_amount = %s WHERE user_id = %s",
					   ('menu', current_time, 'Здесь пока пусто', 'Здесь пока пусто', message.from_user.id))

		# Генерация кнопок и удаление последнего сообщения
		bot.delete_message(message.chat.id, message.message_id)
		markup = types.InlineKeyboardMarkup()
		btn_tests = types.InlineKeyboardButton('Выполнять задания', callback_data='tests')
		btn_profil = types.InlineKeyboardButton('Мой профиль', callback_data='profil')
		btn_feedback = types.InlineKeyboardButton('Оставить отзыв/поддержка', callback_data='feedback')
		markup.row(btn_tests)
		markup.row(btn_profil)
		markup.row(btn_feedback)
		bot.send_message(message.chat.id, "Меню", reply_markup=markup)

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

@bot.callback_query_handler(func=lambda callback: callback.data == 'tests')
def tests(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Здесь будет храниться прошлое состояние пользователя
	# cursor.execute(f"SELECT user_state FROM users WHERE user_id = {callback.from_user.id}")
	# user_state = (cursor.fetchone())[0]

	# Изменяем состояние пользователя на test
	cursor.execute(f"UPDATE users SET user_state = %s WHERE user_id = %s", ('test', callback.from_user.id))

	# Генерация кнопок и удаление последнего сообщения
	bot.delete_message(callback.message.chat.id, callback.message.message_id)
	markup = types.InlineKeyboardMarkup()
	btn_tasks = types.InlineKeyboardButton("Выбрать номер задания", callback_data='choise_questions')
	btn_amount = types.InlineKeyboardButton("Выбрать количество номеров", callback_data='choise_amount')
	btn_go = types.InlineKeyboardButton('Начать', callback_data='go')
	markup.row(btn_tasks)
	markup.row(btn_amount)
	markup.row(btn_go)

	# Получаю данные о заданиях пользователя, потому что пока не понятно зачем
	cursor.execute(f"SELECT selected_questions FROM users WHERE user_id = {callback.from_user.id}")
	selected_questions = cursor.fetchone()[0]
	cursor.execute(f"SELECT selected_amount FROM users WHERE user_id = {callback.from_user.id}")
	selected_amount = cursor.fetchone()[0]

	# Отправляю сообщение к кнопкам с выбранными заданиями
	bot.send_message(callback.message.chat.id, f"Проходить тесты\nВыбрано задание {selected_questions}\nВыбрано количество {selected_amount}", reply_markup=markup)

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

@bot.callback_query_handler(func=lambda callback: callback.data == 'choise_questions')
def choise_questions(callback):

	# Подключаемся к базе данных
	# config = load_config()
	# connection = psycopg2.connect(**config)
	# cursor = connection.cursor()

	# Здесь будет храниться прошлое состояние пользователя
	# cursor.execute(f"SELECT user_state FROM users WHERE user_id = {callback.from_user.id}")
	# user_state = (cursor.fetchone())[0]

	# Менюшка с выбором номера задания
	bot.delete_message(callback.message.chat.id, callback.message.message_id)
	markup = types.InlineKeyboardMarkup()
	btn_task_1 = types.InlineKeyboardButton("1", callback_data='questions_1')
	btn_task_2 = types.InlineKeyboardButton("2", callback_data='questions_2')
	btn_task_3 = types.InlineKeyboardButton("3", callback_data='questions_3')
	markup.row(btn_task_1, btn_task_2, btn_task_3)
	bot.send_message(callback.message.chat.id, "Выберите номер задания", reply_markup=markup)

	# Закрываем соединение с базой данных
	# connection.commit()
	# cursor.close()
	# connection.close()

@bot.callback_query_handler(func=lambda callback: callback.data == 'questions_1')
def return_choise_questions(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_questions = %s WHERE user_id = %s",
				   ('1', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)


@bot.callback_query_handler(func=lambda callback: callback.data == 'questions_2')
def return_choise_questions(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_questions = %s WHERE user_id = %s",
				   ('2', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)
@bot.callback_query_handler(func=lambda callback: callback.data == 'questions_3')
def return_choise_questions(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_questions = %s WHERE user_id = %s",
				   ('3', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)
@bot.callback_query_handler(func=lambda callback: callback.data == 'choise_amount')
def choise_questions(callback):

	# Подключаемся к базе данных
	# config = load_config()
	# connection = psycopg2.connect(**config)
	# cursor = connection.cursor()

	# Здесь будет храниться прошлое состояние пользователя
	# cursor.execute(f"SELECT user_state FROM users WHERE user_id = {callback.from_user.id}")
	# user_state = (cursor.fetchone())[0]

	# Здесь будет редачаться кнопки с выбором количества номеров
	bot.delete_message(callback.message.chat.id, callback.message.message_id)
	markup = types.InlineKeyboardMarkup()
	btn_amount_5 = types.InlineKeyboardButton("5", callback_data='amount_5')
	btn_amount_10= types.InlineKeyboardButton("10", callback_data='amount_10')
	btn_amount_20 = types.InlineKeyboardButton("20", callback_data='amount_20')
	markup.row(btn_amount_5, btn_amount_10, btn_amount_20)
	bot.send_message(callback.message.chat.id, "Выберите количество заданий", reply_markup=markup)

	# Закрываем соединение с базой данных
	# connection.commit()
	# cursor.close()
	# connection.close()

@bot.callback_query_handler(func=lambda callback: callback.data == 'amount_5')
def return_choise_amount(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_amount = %s WHERE user_id = %s",
				   ('5', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)

@bot.callback_query_handler(func=lambda callback: callback.data == 'amount_10')
def return_choise_amount(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_amount = %s WHERE user_id = %s",
				   ('10', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)

@bot.callback_query_handler(func=lambda callback: callback.data == 'amount_20')
def return_choise_amount(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	# Запрос, который меняет задание у пользователя
	cursor.execute(f"UPDATE users SET selected_amount = %s WHERE user_id = %s",
				   ('20', callback.from_user.id))

	# Закрываем соединение с базой данных
	connection.commit()
	cursor.close()
	connection.close()

	# Возвращаемся к основному меню настройки заданий
	tests(callback)

@bot.callback_query_handler(func=lambda callback: callback.data == 'go')
def save_questions(callback):

	# Подключаемся к базе данных
	config = load_config()
	connection = psycopg2.connect(**config)
	cursor = connection.cursor()

	bot.delete_message(callback.message.chat.id, callback.message.message_id)

	# Вызваливаем из базы данных выбранное задание и количество номеров
	cursor.execute(f"SELECT selected_questions FROM users WHERE user_id = {callback.from_user.id}")
	selected_question = cursor.fetchone()[0]
	cursor.execute(f"SELECT selected_amount FROM users WHERE user_id = {callback.from_user.id}")
	selected_amount = cursor.fetchone()[0]

	for i in range(int(selected_amount)):

		# Выбираю id рандомный вопрос
		cursor.execute(f"SELECT id FROM questions WHERE question_id = {selected_question} ORDER BY RANDOM() LIMIT 1;")
		id = (cursor.fetchone())[0]

		# Выбираю правильный ответ к вопросу
		cursor.execute(f"SELECT answer FROM questions WHERE id = %s", (id, ))
		answer_true = cursor.fetchone()[0]


		# Генерирую 7 не правильных ответов
		cursor.execute("SELECT answer FROM questions WHERE question_id = %s and answer != %s ORDER BY RANDOM() LIMIT 7;", (selected_question, answer_true))
		answer_fall = cursor.fetchall()


		# Создаю список, где уже будут все ответы перемешанные и сразу преобразую их в строку
		answer_all = answer_random(answer_true, answer_fall)
		answer_all_string = ""
		for i in answer_all:
			answer_all_string = answer_all_string + " " + i

		cursor.execute("INSERT INTO results (user_id, username, id, question_id, answer_true, answer_all) "
					   "VALUES (%s, %s, %s, %s, %s, %s);",
					   (callback.from_user.id, callback.from_user.username, id, selected_question,	answer_true, answer_all_string))

	# for i in range(int(selected_amount)):
	# 	cursor.execute("")

	connection.commit()
	cursor.close()
	connection.close()

# 	# Сохраняем максимальное количество номеров для данного задания
# 	cursor.execute(f"SELECT COUNT(*) FROM questions WHERE question_id = {int(selected_question)}")
# 	count_of_question = (cursor.fetchone())[0]
#
# 	for i in range(int(selected_amount)):
#
# 		print(i)
# 		# Выбираю рандомный вопрос
# 		cursor.execute(f"SELECT question FROM questions WHERE question_id = {selected_question} ORDER BY RANDOM() LIMIT 1;")
# 		question = (cursor.fetchone())[0]
# 		cursor.execute("INSERT INTO results (id, question_id) VALUES (%s, %s)", ())
#
# 		# Выбираю правильный ответ к вопросу
# 		cursor.execute(f"SELECT answer FROM questions WHERE question = %s", (question, ))
# 		answer_true = cursor.fetchone()[0]
#
# 		# Генерирую 7 не правильных ответов
# 		cursor.execute("SELECT answer FROM questions WHERE question_id = %s and answer != %s ORDER BY RANDOM() LIMIT 7;", (selected_question, answer_true))
# 		answer_fall = cursor.fetchall()
#
# 		send_question(callback, question, answer_true, answer_fall)
#
# def send_question(callback, question, answer_true, answer_fall):
#
# 	# Получаю уже перемешанный список всех ответов
# 	answers_all = answer_random(answer_true, answer_fall)
#
# 	# Дальше идет блок с кнопками ответов
# 	markup = types.InlineKeyboardMarkup()
#
# 	btn_answer_1 = types.InlineKeyboardButton(answers_all[0], callback_data='answer_1')
# 	btn_answer_2 = types.InlineKeyboardButton(answers_all[1], callback_data='answer_2')
# 	btn_answer_3 = types.InlineKeyboardButton(answers_all[2], callback_data='answer_3')
# 	btn_answer_4 = types.InlineKeyboardButton(answers_all[3], callback_data='answer_4')
# 	markup.row(btn_answer_1, btn_answer_2, btn_answer_3, btn_answer_4)
#
# 	btn_answer_5 = types.InlineKeyboardButton(answers_all[4], callback_data='answer_5')
# 	btn_answer_6 = types.InlineKeyboardButton(answers_all[5], callback_data='answer_6')
# 	btn_answer_7 = types.InlineKeyboardButton(answers_all[6], callback_data='answer_7')
# 	btn_answer_8 = types.InlineKeyboardButton(answers_all[7], callback_data='answer_8')
# 	markup.row(btn_answer_5, btn_answer_6, btn_answer_7, btn_answer_8)
#
# 	bot.send_message(callback.message.chat.id, question, reply_markup=markup)
#
# 	# Здесь должна вызывать функция, которая проверяет ответ пользователя
# 	check_answer(callback, question, answer_true)


# @bot.callback_query_handler(func=lambda callback: callback.data == 'answer_1')
# def check_answer(callback, question, answer_true):
#
# 	config = load_config()
# 	connection = psycopg2.connect(**config)
# 	cursor = connection.cursor()
#
# 	cursor.execute("INSERT INTO results (user_id, username, id, question_id, right) VALUES (%s, %s, %s, %s, %s)", (callback.message.from_user.id, ))
#
# "INSERT INTO users (user_id, username, user_state) VALUES (%s, %s, %s) ON CONFLICT (user_id)"
# 							" DO UPDATE SET username = EXCLUDED.username, user_state = EXCLUDED.user_state",
# 						(message.from_user.id, message.from_user.username, 'start')
#
#
bot.infinity_polling()