import json

from telegram.ext import Updater, CommandHandler

updater = Updater("") # сюда нужно вставить токен бота


def start(update, context): #Команда подключения к боту
    user_list = {}
    with open("users.json", "r") as users:
        try:                                #Блок try - except на случай если файл пуст
            user_list = json.load(users)
        except:
            pass
    user_list[update.message.chat.username] = update.message.chat.to_dict()
    with open("users.json", "w") as users:  #Второй раз открываем файл с режимом "w" чтобы перезаписать содержимое
        users.write(json.dumps(user_list))
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Привет!"
    )

def help(update, context): #Стандартная команда подсказки по использованию бота
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Это учебный бот, он собирает данные о пользователях!"
    )

def stop(update, context):  #Команда отключения от бота
    user_list = {}
    with open("users.json", "r") as users:
        user_list = json.load(users)
    user_list.pop(update.message.chat.username, None) #None - значение по умолчанию, в случае если такого пользователя не найдется в списке
    with open("users.json", "w") as users:
        users.write(json.dumps(user_list))
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Прощай, {update.message.chat.first_name}! :('
    )

def user_count(update, context):    #Команда выводящая количество подключенных пользователей
    user_list = {}
    with open("users.json", "r") as users:
        user_list = json.load(users)
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Пользователей подключено: {len(user_list)}'
    )

def describe_me(update, context):   #Команда выводящая информацию о пользователе
    user_list = {}
    with open("users.json", "r") as users:
        user_list = json.load(users)
    me = user_list.get(update.message.chat.username)
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Ваш айди - {me.get("id")}, ваш ник - {me.get("username")}, ваше имя = {me.get("first_name")}!'
    )


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('count', user_count))
updater.dispatcher.add_handler(CommandHandler('describe', describe_me))
updater.start_polling(poll_interval=10.0)
