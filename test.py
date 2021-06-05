import telebot
from telebot import types

import psycopg2

from psycopg2 import OperationalError

bot = telebot.TeleBot('1787414978:AAGvEM4O-G-M5lGOuBsKNTggRJsns5J_-pA')


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection(
    "postgres", "postgres", "postgres", "178.154.246.242", "5432"
)

cursor = connection.cursor()


@bot.message_handler(commands=['start'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Поиск по БИН', callback_data='BIN')
    item2 = types.InlineKeyboardButton('Поиск по ФИО', callback_data='FIO')
    item3 = types.InlineKeyboardButton('Поиск по адресу', callback_data='address')
    markup.add(item, item2, item3)
    bot.send_message(message.chat.id, 'Бот готов к работе', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_bin(call):
    if call.message:
        if call.data == 'BIN':
            msg = bot.send_message(call.message.chat.id, 'Введите БИН')
            bot.register_next_step_handler(msg, askBin)
        if call.message:
            if call.data == 'FIO':
                msg = bot.send_message(call.message.chat.id, 'Введите ФИО (в верхнем регистре)')
                bot.register_next_step_handler(msg, askFio)
        if call.message:
            if call.data == 'address':
                msg = bot.send_message(call.message.chat.id, 'Введите адрес (в верхнем регистре, через запятую)')
                bot.register_next_step_handler(msg, askAdd)


def askBin(message):
    cursor = connection.cursor()
    chat_id = message.chat.id
    bin = message.text
    if not bin.isdigit():
        msg = bot.send_message(chat_id, 'БИН должен быть целым числом. Попробуйте еще раз')
        bot.register_next_step_handler(msg, askBin) #askSource
        return
    else:
        msg = bot.send_message(chat_id, 'Спасибо, идет обработка запроса')
        cursor.execute("SELECT * FROM test.test_1 WHERE value1 = '{}'".format(bin))
        for i in cursor:
            get_sql = i[0]
            get_sql1 = i[1]
            get_sql2 = i[2]
            get_sql4 = i[4]
            get_sql9 = i[9]
            get_sql10 = i[10]
            bot.send_message(chat_id, f'БИН: {get_sql}' 
            f'\nНаименование ЮЛ: {get_sql1}' 
            f'\nДата регистрации ЮЛ: {get_sql2}'
            f'\nВид деятельности ЮЛ: {get_sql4}'
            f'\nЮридический адрес: {get_sql9}'
            f'\nРуководитель: {get_sql10}')
        #connection.close()



def askFio(message):
    cursor = connection.cursor()
    chat_id = message.chat.id
    fio = message.text
    msg = bot.send_message(chat_id, 'Спасибо, идет обработка запроса')
    d = "SELECT * FROM test.test_1 WHERE value11 = '{}'".format(fio)
    cursor.execute(d)
    for i in cursor:
        get_sql = i[0]
        get_sql1 = i[1]
        get_sql2 = i[2]
        get_sql4 = i[4]
        get_sql9 = i[9]
        get_sql10 = i[10]
        if fio in i[10]:
            bot.send_message(chat_id, f'БИН: {get_sql}' 
                f'\nНаименование ЮЛ: {get_sql1}' 
                f'\nДата регистрации ЮЛ: {get_sql2}'
                f'\nВид деятельности ЮЛ: {get_sql4}'
                f'\nЮридический адрес: {get_sql9}'
                f'\nРуководитель: {get_sql10}')
        else:
            bot.send_message(chat_id, 'Ничего не найдено')
            bot.register_next_step_handler(msg, askFio)



def askAdd(message):
    cursor = connection.cursor()
    chat_id = message.chat.id
    addr = message.text
    bot.send_message(chat_id, 'Спасибо, идет обработка запроса')
    d = "SELECT * FROM test.test_1 WHERE value10 like '{}%%'".format(addr)
    cursor.execute(d)
    for i in cursor:
        get_sql = i[0]
        get_sql1 = i[1]
        get_sql2 = i[2]
        get_sql4 = i[4]
        get_sql9 = i[9]
        get_sql10 = i[10]
        if addr in i[9]:
            bot.send_message(chat_id, f'БИН: {get_sql}' 
                f'\nНаименование ЮЛ: {get_sql1}' 
                f'\nДата регистрации ЮЛ: {get_sql2}'
                f'\nВид деятельности ЮЛ: {get_sql4}'
                f'\nЮридический адрес: {get_sql9}'
                f'\nРуководитель: {get_sql10}')
        elif addr not in i[9]:
            bot.send_message(chat_id, 'Ничего не найдено')

bot.polling(none_stop=True)
