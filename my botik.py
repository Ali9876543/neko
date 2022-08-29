import telebot
from telebot import types
import requests, bs4

token = '5420194922:AAE9hM8lI--kdQs8JDrf2UvhslzEIQNuZXk'
bot = telebot.TeleBot(token)


brand = '' # бренд смартфона
price = '' # цена

@bot.message_handler(commands=['start'])
def start(message):
    k = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Apple')
    button2 = types.KeyboardButton('Samsung')
    button3 = types.KeyboardButton('HUAWEI')
    button4 = types.KeyboardButton('OPPO')
    k.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Привет, я бот технодом. Выбери бренд', reply_markup=k)

@bot.message_handler(content_types=['text'])
def brands(message):
    global brand
    if message.text == 'Apple':
        brand = 'f/brands/apple'
    elif message.text == 'Samsung':
        brand = 'f/brands/samsung'
    elif message.text == 'HUAWEI':
        brand = 'f/brands/huawei'
    elif message.text == 'OPPO':
        brand = 'f/brands/oppo'
    m = bot.send_message(message.chat.id, 'Введи ценовой диапазон через тире. Пример, 200000-500000')
    bot.register_next_step_handler(m, prices)
    
def prices(message):
    global brand
    price = message.text.split('-')
    link = f'https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony/{brand}?priceMin={price[0]}&priceMax={price[1]}'
    data = requests.get(link)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    links = soup.findAll('a', class_='category-page-list__item-link')
    for li in links:
        href = li.get('href')
        bot.send_message(message.chat.id, 'https://technodom.kz'+href)

bot.polling()

    
