#%%
import telebot
from telebot.types import ForceReply
import requests
from flask import Flask, request

with open("TOKEN.txt", 'r') as f:
    KEY = f.read()

URL = "http://127.0.0.1:5000"
bot = telebot.TeleBot(KEY, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=URL)
username= ""
password= ""



app = Flask(__name__)
@app.route('/' , methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


def force_reply():
    reply = ForceReply()
    reply.input_field_placeholder = "MewWwW"
    return reply


def username_handler(message):
    global username
    username = message.text
    
    sent_msg = bot.send_message(message.chat.id, f"Enter your Password:", reply_markup=force_reply())
    bot.register_next_step_handler(sent_msg, password_handler)

   
            
def password_handler(message):
    global password
    password = message.text
    requests.post(f"{URL}/driver", json={"username": username, "password": password, "chatid": message.chat.id})


@bot.message_handler(commands=["start", "newInfo"])
def start(message):
    sent_msg = bot.send_message(message.chat.id, "Please Enter your username:", reply_markup=force_reply())
    bot.register_next_step_handler(sent_msg, username_handler)
    


@bot.message_handler(func=lambda message: True)
def recieve_cred(message):
    user_input = message.text
    if len(user_input) == 4:
        r = requests.post(f"{URL}/captcha", json={"captcha":user_input, 'chatid':message.chat.id})
        



#%%


    