import datetime
from telebot import TeleBot, types
from functions import *
import csv

TOKEN = ''
BOT_PATH ='t.me/GB10_bot'

bot = TeleBot(TOKEN)

def new_log_user(msg):
    id_ = msg.from_user.id
    name_ = msg.from_user.full_name
    text = msg.text
    date_ = str(datetime.datetime.now())
    new_log = Log(len(log_list) + 1, id_, name_, date_, text)
    log_list.append(new_log)
    return text, id_

def new_log_bot(msg, text):
    id_ = 0
    name_ = 'bot'
    text = text
    date_ = str(datetime.datetime.now())
    new_log = Log(len(log_list) + 1, id_, name_, date_, text)
    log_list.append(new_log)
    bot.send_message(chat_id=msg.from_user.id, text=text)



@bot.message_handler(content_types=['document'])
def answer(msg: types.Message):
    filename = msg.document.file_name
    with open(filename, 'wb') as file:
        file.write(bot.download_file(bot.get_file(msg.document.file_id).file_path))
    bot.send_message(chat_id=msg.from_user.id, text='Вывожу логыыыы')

    # Можете раскомментировать, если потребуется затем удалять файл после обработки,
    # чтобы не тратить память.
    # Не забудьте импортировать os
    # os.remove(filename)


dct = {}
global log_list
try:
    with open('log.csv', 'r', encoding='utf-8') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=';', skipinitialspace=False)
        log_list = []
        for line, row in enumerate(file_reader):
            log_list.append(Log(row))
except:
    log_list = []


@bot.message_handler(commands=['start', 'help'])
def answer(msg: types.Message):
    dct[msg.from_user.id] = []
    new_log_bot(msg, 'Hello input number (complex format x+yj without spaces)')


@bot.message_handler(commands=['log'])
def answer(msg: types.Message):
    bot.send_message(chat_id=msg.from_user.id, text='Вывожу лог')
    log_text = ''
    for text in log_list:
        log_text += str(text) + '\n'
    bot.send_message(chat_id=msg.from_user.id, text=log_text)


@bot.message_handler()
def answer(msg: types.Message):
    text, id_ = new_log_user(msg)
    if len(dct[id_]) == 0:
        check_result = check_if_number(text)
        if check_result[0]:
            number_type = check_result[1]
            number = number_res(check_result)
            dct[id_].append([number_type, number])
            new_log_bot(msg, 'Input second number (complex format x+yj without spaces)')
        else:
            new_log_bot(msg, 'Error. Input number (complex format x+yj without spaces)')
    elif len(dct[id_]) == 1:
        check_result = check_if_number(text)
        if check_result[0]:
            number_type = check_result[1]
            number = number_res(check_result)
            dct[id_].append([number_type, number])
            new_log_bot(msg, 'Input math action (+ - * : **)')
        else:
            new_log_bot(msg, 'Error. Input second number (complex format x+yj without spaces)')
    else:
        check_result = check_action(text)
        if check_result[0]:
            result = calc_result(id_, dct, check_result[1])
            new_log_bot(msg, result)
            bot.send_message(chat_id=msg.from_user.id, text=f'Результат: {result}')
            dct[id_].clear()
            log_save(log_list)
        else:
            new_log_bot(msg, ' Error. Input math action (+ - * : **)')


bot.polling()


