import telebot
import random
from telebot import types
from urllib import request

bot = telebot.TeleBot("7080956095:AAFjuCS-D-E6yiuf-cGE7bM6DJkszYeA_K4")

class User:
    def __init__(self, chat_id, level=None, word=None, masked_word=None, tries=5):
        self.chat_id = chat_id
        self.level = level
        self.word = word
        self.masked_word = masked_word
        self.tries = tries

users = {}  # Словарь для хранения пользователей и их состояний игры

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот где всё подряд!")

@bot.message_handler(commands=['bukavki'])
def game(message):
    if message.chat.id in users:
        del users[message.chat.id]

    result = request.urlopen("https://calculator888.ru/random-generator/sluchaynoye-slovo")
    data = result.read().decode()
    w1 = '<div class="blok_otvet" id="bov" style="font-size:60px;">'
    start = data.find(w1)
    data = data[start:]
    w2 = "</div>"
    end = data.find(w2)
    word = data[:end].replace(w1, '').strip().lower()

    users[message.chat.id] = User(chat_id=message.chat.id, word=word, masked_word="_" * len(word))
    bot.send_message(message.chat.id, "Загаданное слово: " + users[message.chat.id].masked_word)
    bot.send_message(message.chat.id, str(len(word)) + " букв")
    bot.send_message(message.chat.id, "Введите букву:")

@bot.message_handler(func=lambda message: len(message.text) == 1 and message.text.isalpha())
def check_letter(message):
    if message.chat.id in users:
        user = users[message.chat.id]
        letter = message.text.lower()
        
        if letter in user.word:
            temp_word = "".join([letter if user.word[i] == letter else user.masked_word[i] for i in range(len(user.word))])
            user.masked_word = temp_word
            if temp_word == user.word:
                bot.send_message(message.chat.id, "Загаданное слово: " + temp_word)
                bot.send_message(message.chat.id, "Вы угадали слово! Поздравляю!")
                del users[message.chat.id]
                return
        else:
            user.tries -= 1

        bot.send_message(message.chat.id, "Загаданное слово: " + user.masked_word)
        bot.send_message(message.chat.id, "Осталось попыток: " + str(user.tries))
        bot.send_message(message.chat.id, "А знаете что меньше числа оставшихся попыток? Это цена билетов на aviasales.ru!")
        
        if user.tries == 0:
            bot.send_message(message.chat.id, "У вас закончились попытки. Вы проиграли.")
            del users[message.chat.id]



games = {}  # Dictionary to store game state for each user

@bot.message_handler(commands=['chiselki'])
def number_guessing_game(message):
    chat_id = message.chat.id
    target_number = random.randint(0, 100)
    attempts = 0
    games[chat_id] = {
        'target_number': target_number,
        'attempts': attempts
    }
    
    bot.send_message(chat_id, "Здравствуйте! Добро пожаловать в игру chiselki!")
    bot.send_message(chat_id, "Отправьте число")
    bot.register_next_step_handler(message, handle_guess)

def handle_guess(message):
    chat_id = message.chat.id
    if chat_id not in games:
        return
    
    guess = message.text
    
    if not guess.isdigit():
        bot.send_message(chat_id, "Пожалуйста, введите только число.")
        bot.register_next_step_handler(message, handle_guess)
        return
    
    guess = int(guess)
    target_number = games[chat_id]['target_number']
    games[chat_id]['attempts'] += 1
    
    if guess < target_number:
        bot.send_message(chat_id, "Загаданное число больше введённого")
        bot.register_next_step_handler(message, handle_guess)
    elif guess > target_number:
        bot.send_message(chat_id, "Загаданное число меньше введённого")
        bot.register_next_step_handler(message, handle_guess)
    else:
        bot.send_message(chat_id, f"Поздравляем! Вы угадали число {target_number} за {games[chat_id]['attempts']} попыток")
        del games[chat_id]  # End the game
@bot.message_handler(commands=['number'])
def number(message):
    chat_id = message.chat.id
    number = random.randint(0, 999999999)
    bot.send_message(chat_id, number)
@bot.message_handler(commands=['word'])
def word(message):
    chat_id = message.chat.id
    result = request.urlopen("https://calculator888.ru/random-generator/sluchaynoye-slovo")
    data = result.read().decode()
    w1 = '<div class="blok_otvet" id="bov" style="font-size:60px;">'
    start = data.find(w1)
    data = data[start:]
    w2 = "</div>"
    end = data.find(w2)
    wordd = data[:end].replace(w1, '').strip().lower()
    bot.send_message(chat_id, wordd)

@bot.message_handler(commands=['patriot'])
def patriot(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Здравствуйте! Добро пожаловать в патриотизатор текста!")
    bot.send_message(chat_id, "Отправьте текст, который нужно патриотизировать.")
    bot.register_next_step_handler(message, petriot)

def petriot(message):
    chat_id = message.chat.id
    text = message.text
    ao=text.replace("сво", "СВО")
    c=ao.replace("Сво", "СВО")
    e=c.replace("В", "V")
    a=c.replace("з", "Z")
    b=a.replace("в", "V")
    d=b.replace("З", "Z")
    bot.send_message(chat_id, "🇷🇺🇷🇺🇷🇺" + d + "🇷🇺🇷🇺🇷🇺")

bot.polling()
