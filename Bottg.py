import telebot
from telebot import types
import time
import random

# Инициализация бота
TOKEN = "6763204256:AAEPsrEOtIqIeGg5t8Da1Ba8RXjGWliOnuA"
bot = telebot.TeleBot(TOKEN)

# Список администраторов
admins = set([7069906494])

# Хранение состояний пользователей
mute_status = {}
banned_users = {}
warn_count = {}
welcome_message = "Добро пожаловать в чат!"
jokes = ["Шутка 1", "Шутка 2", "Шутка 3"]
anecdotes = ["Анекдот 1", "Анекдот 2", "Анекдот 3"]
facts = ["Интересный факт 1", "Интересный факт 2", "Интересный факт 3"]

# Команда для получения списка администраторов
@bot.message_handler(commands=['admins'])
def list_admins(message):
    if message.from_user.id in admins:
        admins_list = "\n".join(map(str, admins))
        bot.reply_to(message, f"Список администраторов:\n{admins_list}")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для проверки статуса пользователя
@bot.message_handler(commands=['status'])
def check_status(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            status = []
            
            if user_id in mute_status:
                status.append("Пользователь в мутах.")
            if user_id in banned_users:
                status.append("Пользователь забанен.")
            if user_id in warn_count:
                status.append(f"Количество варнов: {warn_count[user_id]}")
                
            if not status:
                bot.reply_to(message, f"Статус пользователя {user_id}: чист.")
            else:
                bot.reply_to(message, f"Статус пользователя {user_id}: {', '.join(status)}")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /status <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для сброса варнов пользователя
@bot.message_handler(commands=['clear_warnings'])
def clear_warnings(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            if user_id in warn_count:
                del warn_count[user_id]
                bot.reply_to(message, f"Варны пользователя {user_id} сброшены.")
            else:
                bot.reply_to(message, f"У пользователя {user_id} нет варнов.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /clear_warnings <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для отправки сообщения всем пользователям
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id in admins:
        msg = message.text[len("/broadcast "):]
        if msg:
            for user_id in mute_status.keys():
                try:
                    bot.send_message(user_id, msg)
                except:
                    continue
            bot.reply_to(message, "Сообщение отправлено всем пользователям.")
        else:
            bot.reply_to(message, "Вы не указали сообщение для рассылки.")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для проверки состояния бота
@bot.message_handler(commands=['status_bot'])
def status_bot(message):
    if message.from_user.id in admins:
        muted_count = len(mute_status)
        banned_count = len(banned_users)
        bot.reply_to(message, f"Состояние бота:\nЗамученные: {muted_count}\nЗабаненные: {banned_count}")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для установки приветственного сообщения
@bot.message_handler(commands=['set_welcome'])
def set_welcome(message):
    if message.from_user.id in admins:
        welcome_msg = message.text[len("/set_welcome "):]
        if welcome_msg:
            global welcome_message
            welcome_message = welcome_msg
            bot.reply_to(message, "Приветственное сообщение обновлено.")
        else:
            bot.reply_to(message, "Вы не указали сообщение.")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для показа текущего приветственного сообщения
@bot.message_handler(commands=['show_welcome'])
def show_welcome(message):
    if message.from_user.id in admins:
        bot.reply_to(message, f"Текущее приветственное сообщение: {welcome_message}")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для очистки статуса всех замученных пользователей
@bot.message_handler(commands=['clear_mutes'])
def clear_mutes(message):
    if message.from_user.id in admins:
        mute_status.clear()
        bot.reply_to(message, "Статусы всех замученных пользователей очищены.")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Обработка новых участников
@bot.ChatMemberUpdated
def welcome_new_member(message):
    if message.new_chat_member.status == "member":
        bot.send_message(message.chat.id, welcome_message)

# Команда /joke
@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, random.choice(jokes))

# Команда /anecdote
@bot.message_handler(commands=['anecdote'])
def send_anecdote(message):
    bot.reply_to(message, random.choice(anecdotes))

# Команда /random_number
@bot.message_handler(commands=['random_number'])
def send_random_number(message):
    number = random.randint(1, 100)
    bot.reply_to(message, f'Случайное число: {number}')

# Команда /fact
@bot.message_handler(commands=['fact'])
def send_fact(message):
    bot.reply_to(message, random.choice(facts))

# Проверка состояний пользователей
@bot.message_handler(func=lambda message: True)
def check_user_status(message):
    user_id = message.from_user.id

    # Проверка мута
    if user_id in mute_status:
        if time.time() < mute_status[user_id]:
            bot.delete_message(message.chat.id, message.message_id)
            return
        else:
            del mute_status[user_id]

    # Проверка бана
    if user_id in banned_users:
        if time.time() < banned_users[user_id]:
            bot.kick_chat_member(message.chat.id, user_id)
            return
        else:
            del banned_users[user_id]

# Запуск бота
bot.polling(none_stop=True)
