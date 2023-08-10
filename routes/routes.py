from flask import Flask
from threading import Thread
from googletrans import Translator
from routes.parses import get_all_skins

app = Flask('')
translator = Translator()


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()


def execute(bot, message):
    skins = get_all_skins()

    for skin in skins:
        bot.send_photo(message.chat.id,
                       skin['image'],
                        caption = skin['text']
        )
