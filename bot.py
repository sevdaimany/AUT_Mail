#%%
import telebot
from telebot.types import ForceReply
from bs4 import BeautifulSoup as bs
import requests
import json


KEY = "5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw"
bot = telebot.TeleBot(KEY)
username= ""
password=""

def force_reply():
    reply = ForceReply()
    reply.input_field_placeholder = "Username and password with ,"
    return reply


def username_handler(message):
    global username
    username = message.text
    sent_msg = bot.send_message(message.chat.id, f"Your username is {username}. what is your password?")
    bot.register_next_step_handler(sent_msg, password_handler)
   
            
def password_handler(message):
    global password
    password = message.text
    bot.send_message(message.chat.id, f"Your password is {password}")
    requests.post("http://10.10.10.175:5000/driver", json={"username": username, "password": password, "chatid": message.chat.id})




@bot.message_handler(commands=["start"])
def start(message):
    sent_msg = bot.send_message(message.chat.id, "Please Enter your username:")
    bot.register_next_step_handler(sent_msg, username_handler)
    
    
            
            
            
  

def send_unseen_emails(message, allEmails, newEmailIDs):
    for email in allEmails:
        if email["isSeen"] == "no" and (email["id"] in newEmailIDs):
            text = f"From : {email['from']}\nSubject : {email['subject']}\nSnippet : {email['snippet']}\nDate: {email['date']}"
            bot.send_message(message.chat.id, text)




@bot.message_handler(func=lambda message: True)
def recieve_cred(message):
    username_input = message.text
    requests.post("http://10.10.10.175:5000/captcha", json={"captcha":username_input })
        


bot.polling()

#%%


    