import telebot
from telebot import types
import time
import random

# Инициализация бота
TOKEN = "YOUR_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# Список администраторов (включите своего админа для первоначального запуска)
admins = {6321157988}

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
    "Каждый год мы теряем около 70% своих вкусовых рецепторов.",
    "Единственная часть тела, которая не имеет кровоснабжения, - роговица глаза. Кислород она получает непосредственно из воздуха.",
    "Емкость мозга человека превышает 4 терабайта.",
    "До 7 месяцев ребенок может дышать и глотать одновременно.",
    "Ваш череп состоит из 29 различных костей.",
    "При чихании все функции организма останавливаются, даже сердце.",
    "Один человеческий мозг генерирует больше электрических импульсов в течение одного дня, чем все телефоны мира, вместе взятые."
]

def get_user_id(username):
    """Получить user_id по юзернейму"""
    try:
        user = bot.get_chat(username)
        return user.id
    except Exception as e:
        return None

# Команда для получения списка команд
@bot.message_handler(commands=['commands'])
def list_commands(message):
    command_list = """
    Доступные команды:
    /addadm <username> - Добавить администратора
    /mute <username> <duration> [причина] - Замучить пользователя на указанный срок
    /unmute <username> - Размутить пользователя
    /ban <username> <duration> [причина] - Забанить пользователя на указанный срок
    /unban <username> - Разбанить пользователя
    /warn <username> [причина] - Выдать варн пользователю
    /unwarn <username> - Снять варн у пользователя
    /kick <username> [причина] - Кикнуть пользователя из чата
    /admins - Показать список администраторов
    /joke - Получить случайный анекдот
    /fact - Получить случайный факт
    """
    bot.reply_to(message, command_list)

# Команда для получения списка администраторов
@bot.message_handler(commands=['admins'])
def list_admins(message):
    admin_list = "\n".join(f"@{bot.get_chat(admin).username}" for admin in admins if bot.get_chat(admin).username)
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
            username = message.text.split()[1]
            user_id = get_user_id(username)
            if user_id is not None:
                admins.add(user_id)
                bot.reply_to(message, f"Пользователь {username} добавлен в администраторы.")
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except IndexError:
            bot.reply_to(message, "Используйте: /addadm <username>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для мута
@bot.message_handler(commands=['mute'])
def mute(message):
    if message.from_user.id in admins:
        try:
            parts = message.text.split()
            username = parts[1]
            duration = int(parts[2])
            reason = " ".join(parts[3:]) if len(parts) > 3 else "Причина не указана"
            user_id = get_user_id(username)
            if user_id is not None:
                mute_status[user_id] = (time.time() + duration)
                bot.reply_to(message, f"Пользователь {username} был замучен на {duration} секунд. Причина: {reason}.")
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /mute <username> <duration> [причина]")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для размута
@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.from_user.id in admins:
        try:
            username = message.text.split()[1]
            user_id = get_user_id(username)
            if user_id is not None and user_id in mute_status:
                del mute_status[user_id]
                bot.reply_to(message, f"Пользователь {username} был размучен.")
            else:
                bot.reply_to(message, f"Пользователь не найден или не замучен.")
        except IndexError:
            bot.reply_to(message, "Используйте: /unmute <username>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для бана
@bot.message_handler(commands=['ban'])
def ban(message):
    if message.from_user.id in admins:
        try:
            parts = message.text.split()
            username = parts[1]
            duration = int(parts[2])
            reason = " ".join(parts[3:]) if len(parts) > 3 else "Причина не указана"
            user_id = get_user_id(username)
            if user_id is not None:
                banned_users[user_id] = (time.time() + duration)
                bot.reply_to(message, f"Пользователь {username} был забанен на {duration} секунд. Причина: {reason}.")
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /ban <username> <duration> [причина]")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для разбанивания
@bot.message_handler(commands=['unban'])
def unban(message):
    if message.from_user.id in admins:
        try:
            username = message.text.split()[1]
            user_id = get_user_id(username)
            if user_id is not None and user_id in banned_users:
                del banned_users[user_id]
                bot.reply_to(message, f"Пользователь {username} был разбанен.")
            else:
                bot.reply_to(message, f"Пользователь не найден или не забанен.")
        except IndexError:
            bot.reply_to(message, "Используйте: /unban <username>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для варна
@bot.message_handler(commands=['warn'])
def warn(message):
    if message.from_user.id in admins:
        try:
            parts = message.text.split()
            username = parts[1]
            reason = " ".join(parts[2:]) if len(parts) > 2 else "Причина не указана"
            user_id = get_user_id(username)
            if user_id is not None:
                warn_count[user_id] = warn_count.get(user_id, 0) + 1
                bot.reply_to(message, f"Пользователь {username} получил варн. Всего варнов: {warn_count[user_id]}. Причина: {reason}.")

                # Проверка на три варна
                if warn_count[user_id] >= 3:
                    ban_duration = 31536000  # Например, 1 год
                    banned_users[user_id] = (time.time() + ban_duration)
                    bot.reply_to(message, f"Пользователь {username} был забанен на 1 год за 3 варна.")
                    del warn_count[user_id]  # Сбросить счетчик варнов
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /warn <username> [причина]")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для снятия варна
@bot.message_handler(commands=['unwarn'])
def unwarn(message):
    if message.from_user.id in admins:
        try:
            username = message.text.split()[1]
            user_id = get_user_id(username)
            if user_id is not None:
                if user_id in warn_count and warn_count[user_id] > 0:
                    warn_count[user_id] -= 1
                    bot.reply_to(message, f"Варн у пользователя {username} снят. Осталось варнов: {warn_count[user_id]}.")
                else:
                    bot.reply_to(message, f"У пользователя {username} нет варнов для снятия.")
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /unwarn <username>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для кика
@bot.message_handler(commands=['kick'])
def kick(message):
    if message.from_user.id in admins:
        try:
            parts = message.text.split()
            username = parts[1]
            reason = " ".join(parts[2:]) if len(parts) > 2 else "Причина не указана"
            user_id = get_user_id(username)
            if user_id is not None:
                bot.kick_chat_member(message.chat.id, user_id)
                bot.reply_to(message, f"Пользователь {username} был кикнут из чата. Причина: {reason}.")
            else:
                bot.reply_to(message, "Пользователь не найден.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /kick <username> [причина]")
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
