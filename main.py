import telebot
import configparser
import os
from openai import OpenAI
from models import MessageHistory

def jubeseek_bot():
    class ExHandler(telebot.ExceptionHandler):
        def handle(self, error):
            print('Error: ', error)
            return True
    
    dir_path = (os.path.dirname(__file__))
    print("Started at: ", dir_path)

    config = configparser.ConfigParser()
    config.read(f'{dir_path}/settings.ini')

    allowed_users = list(map(int, config['General']['allowed_users'].split(',')))
    bot = telebot.TeleBot(config['General']['bot_token'], exception_handler=ExHandler())
    api_token = config['General']['api_token']
    client = OpenAI(api_key=api_token, base_url="https://api.deepseek.com")

    message_hists = []
    for user in allowed_users:
        message_hists.append(MessageHistory(user))

    def find_history(user):
        for elem in message_hists:
            if user == elem.user:
                return elem

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.from_user.id in allowed_users:
            bot.send_message(message.chat.id, 'Привет, человек! Начнем?') 

    @bot.message_handler(content_types=["text"])
    def process_text(message):
        if message.from_user.id in allowed_users:
            message_hist = find_history(message.from_user.id)
            message_hist.add_message(message.text)

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=message_hist.messages,
            )

            message_hist.messages.append(response.choices[0].message)
            bot.send_message(message.chat.id, response.choices[0].message)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    jubeseek_bot()