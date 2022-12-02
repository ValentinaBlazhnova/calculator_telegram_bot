# В телеграм начинает работать со /start

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = Bot(token='5863649836:AAF_x6Q8-vNKwjSK3SxerxNKWvdP9QogZJ0')
updater = Updater(token='5863649836:AAF_x6Q8-vNKwjSK3SxerxNKWvdP9QogZJ0')
dispatcher = updater.dispatcher

def start(update, context): 
    context.bot.send_message(update.effective_chat.id, "Введите выражение, которое необходимо высчитать: ")

def button_click(update, context): #Запуск отсюда
    separate_expression = parse(update) 
    result = calculate(separate_expression)
    log(separate_expression, result, update)
    view_result(update, context, result) #вывод результата
    
def log(separate_expression, result, update):
    id_user = update.effective_chat.id
    expression = ' '.join(map(str, separate_expression))
    with open('log_expression.txt', 'a') as data:
        data.write(f'{id_user}: {expression} = {result}\n')

def view_result(update, context,data):
    context.bot.send_message(update.effective_chat.id, f' = {data}')

def parse(update):
    expression = update.message.text
    result = []
    number = ''
    # expression = expression.split()
    for symbol in expression:
        if symbol.isdigit():
            number += symbol
        else:
            result.append(float(number))
            number = ''
            result.append(symbol)
    else:
        if number:
            result.append(float(number))
    return result

def calculate(lst):
    result = 0.0
    while '/' in lst:
        index = lst.index('/')
        result = lst[index - 1] / lst[index + 1]
        lst = lst[:index -1] + [result] + lst[index + 2:]
    while '*' in lst:
        index = lst.index('*')
        result = lst[index - 1] * lst[index + 1]
        lst = lst[:index -1] + [result] + lst[index + 2:]
    while '+' in lst:
        index = lst.index('+')
        result = lst[index - 1] + lst[index + 1]
        lst = lst[:index -1] + [result] + lst[index + 2:]
    while '-' in lst:
        index = lst.index('-')
        result = lst[index - 1] - lst[index + 1]
        lst = lst[:index -1] + [result] + lst[index + 2:]
    return result


start_handler = CommandHandler("start", start)
button_click_handler = MessageHandler(Filters.text, button_click)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_click_handler)

updater.start_polling()
updater.idle()
