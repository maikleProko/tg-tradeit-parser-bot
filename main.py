from telebot import types
import constants
from routes.routes import keep_alive, execute
from utils.switch import switch
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot

bot = telebot.TeleBot(constants.TOKEN)

options = {
    'mode': 'default'
}


def change_mode(mode, message, answer):
    options['mode'] = mode
    bot.send_message(message.from_user.id, answer)


def change_options(option, message):
    options[option] = message.text


def send_start_message(message):
    markup = types.ReplyKeyboardMarkup()
    get_button = types.KeyboardButton(constants.GET_BUTTON)
    markup.add(get_button)
    bot.send_message(message.from_user.id, constants.START_MESSAGE, reply_markup=markup)


def process_message(message, current_mode):
    for case in switch(message.text, current_mode):
        if case('/start', 'default'):
            send_start_message(message)
            break
        if case('/get','default'):
            execute(bot, message)
            break
        if case():
            break


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    process_message(message, options['mode'])


keep_alive()
bot.polling(non_stop=True, interval=0)
