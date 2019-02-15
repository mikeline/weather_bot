# weather bot

import urllib.request as urllib2

import telebot

import constants

import json

import string

import time


bot = telebot.TeleBot(constants.token)


def log(message, answer):
    print("\n -----")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print(answer)


def search_weather(latitude, longitude):
    try:
        open_weather_map_result = json.loads(urllib2.urlopen(constants.url_open_weather_map + 'lat=' + str(latitude) + '&lon=' + str(longitude) + '&units=metric'
                                                             '&APPID=' + constants.api).read())
        reply = 'Place: ' + open_weather_map_result['name'] + '\nIt is ' + str(open_weather_map_result['weather'][0]['description']) + ' and ' + \
                str(open_weather_map_result['main']['temp']) + ' C outside'
        print(reply)
        return reply

    except KeyError:
        print("Key error")
        return 'Not found'




@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row("/start", "/stop")
    user_markup.row("photo", "weather", "documents")
    user_markup.row("sticker", "video", "voice", "location")
    bot.send_message(message.from_user.id, "Welcome...", reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "...", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.from_user.id, "My name is WeatherBot and you can ask me what weather it is outside \n"
                                           "Just ask me like: What is the weather outside?")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "hi":
        if message.from_user.first_name == "s":
            gif = open('forsabira.gif', 'rb')
            answer = "Hi, Sabira. Misha just asked me to send you some gif.\n" + "And he also says he is really sorry.."
            bot.send_message(message.from_user.id, answer)
            bot.send_document(message.from_user.id, gif)
            answer = 'gif'
            log(message, answer)
        else:
            answer = "Hi"
            bot.send_message(message.from_user.id, answer)
            log(message, answer)
    elif message.text.lower() == "how are you?":
        answer = "I'm good"
        bot.send_message(message.from_user.id, answer)
        log(message, answer)
    elif message.text.lower() == "weather" or message.text.lower() == "what is the weather outside?":
        answer = "Send me your location"
        bot.send_message(message.from_user.id, answer)
    elif message.text.lower() == "thanks" or message.text.lower() == "thank you":
        answer = "You are welcome"
        bot.send_message(message.from_user.id, answer)
    else:
        answer = "Sorry, didn't get it"
        bot.send_message(message.from_user.id, answer)
        log(message, answer)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    report = search_weather(message.location.latitude, message.location.longitude)
    bot.send_message(message.from_user.id, str(report))
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))


while True:

    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)



