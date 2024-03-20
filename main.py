import telebot
import random
from telebot import types
from urllib import request
from PIL import Image  
from io import BytesIO
import pytesseract

bot = telebot.TeleBot("TELEBOT_API")

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
        print(user.word)
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
            bot.send_message(message.chat.id, "У вас закончились попытки. Вы проиграли. Загаданное слово было: " + str(user.word))
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


import os

@bot.message_handler(commands=['photo'])
def phota(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Отправьте мне любую картинку.")
    bot.register_next_step_handler(message, convert_to_symbols)

def convert_to_symbols(message):
    # Get the photo
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Process the image
    image = Image.open(BytesIO(downloaded_file))
    
    # Limit the image size
    max_image_size = 800
    width, height = image.size
    if width > max_image_size or height > max_image_size:
        max_dimension = max(width, height)
        factor = max_dimension / max_image_size
        new_width = int(width / factor)
        new_height = int(height / factor)
        image = image.resize((new_width, new_height))
    
    # Define the ASCII characters
    ascii_chars = '@%#*+=-:. '
    
    ascii_image = ''
    for y in range(image.size[1]):  # height
        line = ''
        for x in range(image.size[0]):  # width
            pixel = image.getpixel((x, y))
            brightness = sum(pixel) / 3
            line += ascii_chars[int(brightness / 256 * len(ascii_chars))]
        ascii_image += line + '\n'
    
    # Save ASCII art to a text file
    file_path = 'ascii_art.txt'
    with open(file_path, 'w') as file:
        file.write(ascii_image)
    
    # Send the text file to the user
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)
    
    # Clean up - Delete the text file
    os.remove(file_path)


# Dictionary to store user language preferences (can be saved in a database for persistence)
user_languages = {}

# Function to handle incoming messages
@bot.message_handler(commands=['textphoto'])
def handle_ocr(message):
    # Проверка наличия кода языка в команде пользователя
    if len(message.text.split(' ')) > 1:
        lang_code = message.text.split(' ', 1)[1].strip()
        if is_valid_language(lang_code):
            user_languages[message.chat.id] = lang_code
            bot.reply_to(message, f"Язык установлен на {lang_code}. Пожалуйста, отправьте фото для извлечения текста.")
            bot.register_next_step_handler(message, textphoto)
        else:
            bot.reply_to(message, "Неверный код языка. Пожалуйста, укажите допустимый код языка.")
    else:
        bot.reply_to(message, "Используйте команду '/textphoto <код_языка>' для установки языка. Например, '/textphoto eng' для английского.")

# Функция для проверки кода языка
def is_valid_language(lang_code):
    # Добавьте свою логику проверки здесь для кодов языка
    valid_languages = ["eng", "deu", "fra", "spa", "ita", "por", "nld", "rus", "jpn", "kor", "chi_sim", "chi_tra"]  # Примеры допустимых кодов языков
    if lang_code in valid_languages:
        return True
    else:
        return False

# Функция для обработки входящих изображений и извлечения текста
def textphoto(message):
    user_id = message.chat.id
    if user_id in user_languages:
        lang = user_languages[user_id]
    else:
        lang = 'eng'  # Язык по умолчанию, если пользователь не укажет иной

    extracted_text = extract_text_from_image(message, lang)

    # Отправляем извлеченный текст пользователю
    bot.reply_to(message, f"Текст из картинки:\n\n{extracted_text}")
# Функция для извлечения текста из изображения
def extract_text_from_image(message, lang='eng'):
    # Получаем идентификатор фото самого большого размера
    file_id = message.photo[-1].file_id
    # Загружаем фото
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Используем BytesIO для работы с файлом в памяти
    image = Image.open(BytesIO(downloaded_file))
    # Используем Tesseract OCR для извлечения текста из изображения с указанным языком
    text = pytesseract.image_to_string(image, lang=lang)

    return text
bot.polling()
