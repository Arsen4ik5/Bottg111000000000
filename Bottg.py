import telebot
from telebot import types
import time
import random

# Инициализация бота
TOKEN = "6763204256:AAEPsrEOtIqIeGg5t8Da1Ba8RXjGWliOnuA"
bot = telebot.TeleBot(TOKEN)

# Список администраторов
admins = {7069906494}

# Хранение состояний пользователей
mute_status = {}
banned_users = {}
warn_count = {}

# Примеры анекдотов и фактов
jokes = [
    "Почему программисты ненавидят природу? Потому что в ней слишком много ошибок.",
    "Почему у программиста не бывает девушки? Потому что у него есть только один 'интерфейс'.",
    "Какой язык программирования такой же сложный, как и русский? Вводный."
]

facts = [
    "В среднем человек проведет 6 месяцев своей жизни на красный свет светофора.",
    "Около 25% костей человека находятся в руках и ногах.",
    "Каждый год мы теряем около 70% своих вкусовых рецепторов."
"Единственная часть тела, которая не имеет кровоснабжения, - роговица глаза. Кислород она получает непосредственно из воздуха."
"Емкость мозга человека превышает 4 терабайта."
"До 7 месяцев ребенок может дышать и глотать одновременно."
"Ваш череп состоит из 29 различных костей."
"При чихании все функции организма останавливаются, даже сердце."
"Один человеческий мозг генерирует больше электрических импульсов в течение одного дня, чем все телефоны мира, вместе взятые."
]

# Команда для получения списка команд
@bot.message_handler(commands=['commands'])
def list_commands(message):
    command_list = """
    Доступные команды:
    /addadm <user_id> - Добавить администратора
    /mute <user_id> <duration> - Замучить пользователя на указанный срок (в секундах)
    /unmute <user_id> - Размутить пользователя
    /ban <user_id> <duration> - Забанить пользователя на указанный срок (в секундах)
    /unban <user_id> - Разбанить пользователя
    /warn <user_id> - Выдать варн пользователю
    /kick <user_id> - Кикнуть пользователя из чата
    /admins - Показать список администраторов
    /joke - Получить случайный анекдот
    /fact - Получить случайный факт
    """
    bot.reply_to(message, command_list)

# Команда для получения списка администраторов
@bot.message_handler(commands=['admins'])
def list_admins(message):
    admin_list = "\n".join(str(admin) for admin in admins)
    bot.reply_to(message, f"Список администраторов:\n{admin_list}")

# Команда для случайного анекдота
@bot.message_handler(commands=['joke'])
def random_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# Команда для случайного факта
@bot.message_handler(commands=['fact'])
def random_fact(message):
    fact = random.choice(facts)
    bot.reply_to(message, fact)

# Команда для добавления администраторов
@bot.message_handler(commands=['addadm'])
def add_admin(message):
    if message.from_user.id in admins:
        try:
            new_admin_id = int(message.text.split()[1])
            admins.add(new_admin_id)
            bot.reply_to(message, f"Пользователь {new_admin_id} добавлен в администраторы.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /addadm <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для мута
@bot.message_handler(commands=['mute'])
def mute(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            duration = int(message.text.split()[2])
            mute_status[user_id] = (time.time() + duration)
            bot.reply_to(message, f"Пользователь {user_id} был замучен на {duration} секунд.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /mute <user_id> <duration>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для размута
@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            if user_id in mute_status:
                del mute_status[user_id]
                bot.reply_to(message, f"Пользователь {user_id} был размучен.")
            else:
                bot.reply_to(message, f"Пользователь {user_id} не замучен.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /unmute <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для бана
@bot.message_handler(commands=['ban'])
def ban(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            duration = int(message.text.split()[2])
            banned_users[user_id] = (time.time() + duration)
            bot.reply_to(message, f"Пользователь {user_id} был забанен на {duration} секунд.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /ban <user_id> <duration>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для разбанивания
@bot.message_handler(commands=['unban'])
def unban(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            if user_id in banned_users:
                del banned_users[user_id]
                bot.reply_to(message, f"Пользователь {user_id} был разбанен.")
            else:
                bot.reply_to(message, f"Пользователь {user_id} не забанен.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /unban <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для варна
@bot.message_handler(commands=['warn'])
def warn(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            warn_count[user_id] = warn_count.get(user_id, 0) + 1
            bot.reply_to(message, f"Пользователь {user_id} получил варн. Всего варнов: {warn_count[user_id]}")
            
            # Проверка на три варна
            if warn_count[user_id] >= 3:
                ban_duration = 31536000  # Например, 1 час
                banned_users[user_id] = (time.time() + ban_duration)
                bot.reply_to(message, f"Пользователь {user_id} был забанен на 1 год за 3 варна.")
                del warn_count[user_id]  # Сбросить счетчик варнов
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /warn <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для кика
@bot.message_handler(commands=['kick'])
def kick(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            bot.kick_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"Пользователь {user_id} был кикнут из чата.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /kick <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

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
