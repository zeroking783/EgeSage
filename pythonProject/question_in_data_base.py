# import psycopg2
# from connect import *
# from questions_id import *
#
# def questions_in_data_base(questions_id):
#
#     table = questions_id["table"]
#     items_list = list(questions_id.items())
#
#     config = load_config()
#     connection = psycopg2.connect(**config)
#     cursor = connection.cursor()
#
#     # Создаю базу данных для заполнения, если ее еще нет
#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id SERIAL PRIMARY KEY, question VARCHAR(128) NOT NULL, answer VARCHAR(4) NOT NULL);")
#     cursor.execute(f"DELETE FROM {table};")
#     cursor.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;")
#
#     # Заполняю базу данных вопросами и ответами
#     for key, value in items_list[1:]:
#         cursor.execute(
#             f"INSERT INTO {table} (question, answer) VALUES (%s, %s);",(key, value)
#         )
#
#     connection.commit()
#     cursor.close()
#     connection.close()
#
# questions_in_data_base(questions_1)
#

import psycopg2
from connect import *
from questions_id import *

def questions_in_data_base(questions_id):

    question_id = questions_id["question"]
    items_list = list(questions_id.items())

    config = load_config()
    connection = psycopg2.connect(**config)
    cursor = connection.cursor()

    # Заполняю базу данных вопросами и ответами
    for key, value in items_list[1:]:
        cursor.execute(
            f"INSERT INTO questions (question_id, question, answer) VALUES (%s, %s, %s) ON CONFLICT (question) DO NOTHING;",
            (question_id, key, value))

    connection.commit()
    cursor.close()
    connection.close()

questions_in_data_base(questions_1)