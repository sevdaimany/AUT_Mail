from ast import arg
from flask import Flask
from flask_restful import  Api
from flask import  request
import requests
import random
import time
import json
from Models import User
import threading


app = Flask(__name__)
api = Api(app)

URL = "https://webmail.aut.ac.ir"

with open("TOKEN.txt", 'r') as f:
    KEY = f.read()

users = []
threads = []

@app.route('/driver', methods=["POST"])
def start():
    userinfo = request.json
    USERNAME = userinfo["username"]
    PASS = userinfo["password"]
    chatID = userinfo["chatid"]
    user = User(USERNAME, PASS, chatID)
    #Get captcha from webmail
    users.append(user)
    captcha_filename = get_captcha(user)
    #Send captcha to bot
    send_captcha(user,captcha_filename)
     
    return "DONE", 200

 
    
# Should provide it's chat_id in the captcha 
@app.route('/captcha', methods=["POST"])
def solve_captcha():
    chat_id = request.json['chatid']
    for us in users:
        if us.chat_ID == chat_id:
            captcha_input = request.json["captcha"]
            us.captcha_text = captcha_input
            status= login(us)
            if status:
                t1 = threading.Thread(target = user_thread, args = (us,))
                threads.append(t1)
                t1.start()
                # user_thread(us)
            return captcha_input, 200
    return "Not a valid user", 400

def get_captcha(user):
    rand = str(random.randint(1,10000))
    r1 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=isRequired&username={user.username}")
    r2 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=show&username={user.username}")
    user.captcha_id = r2.headers['Set-Cookie'].split(";")[0].split("=")[1]
    file = open(f"./captcha/{rand}.png", "wb")
    file.write(r2.content)
    file.close()
    return rand
    
def send_captcha(user,filename):
    data = {"chat_id": user.chat_ID}
    url = f"https://api.telegram.org/bot{KEY}/sendPhoto" 
    with open(f"./captcha/{filename}.png", "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})  
    send_message(user, "Please Enter the captcha")  
    

def send_sicker(user, filename):
    data = {"chat_id": user.chat_ID}
    url = f"https://api.telegram.org/bot{KEY}/sendSticker" 
    with open(f"./stickers/{filename}.webp", "rb") as sticker_file:
        ret = requests.post(url, data=data, files={"photo": sticker_file})  
    
      
def get_all_emails(user):
    login = requests.post(user.url, data=user.payload, headers=user.header)
    if "Set-Cookie" in dict(login.headers).keys():
        return None
    else:
        returned = "{" + '"MailObject" :' +  login.text[112:] 
        returned = json.loads(returned)
        allEmails = returned["MailObject"]
        return allEmails
  
def login(user):
    data = {
    "action":"login",
    "username":user.username,
    "password": user.password,
    "captchaId":user.captcha_id,
    "captchaText":user.captcha_text
    }
    
    login = requests.post("https://webmail.aut.ac.ir/", data=data)
    if "Set-Cookie" in dict(login.headers).keys():
        send_message(user, "I GOT WRONG INFO!")
        send_sicker(user, "wronginfo")
        send_message(user,"/newInfo - to correct your inforamtion")
        
        return False
    else:
        h = login.text[-230:].split('src="')[1].split("&")[0]
        hmail = login.history[0].headers["Set-Cookie"].split(";")[0].split("=")[1]
        rebuiltCookie = f"passwordExpireWarning=true;displayMoreContent=false;theme=breeze;readingPane=east;_hmail={hmail};_captchaid={user.captcha_id};public_language=en"
        header = {"cookie": rebuiltCookie, "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}  
        payload = {"folderId":"84729550_134979500", "start":0, "limit":50, "sort":"receivedDateUTC", "dir":"DESC", "operation":"MailList"} 
        url = "https://webmail.aut.ac.ir/api/mail/list" + h

        user.url = url
        user.payload = payload
        user.header = header
        return True



    

def send_message(user, text):
    f = requests.post(f"https://api.telegram.org/bot{KEY}/sendMessage" ,json={
            'chat_id':user.chat_ID,
            'text':text,
            }, timeout=3)
    return f

def get_email_ids(allEmails):
    
    ids = []
    for email in allEmails:
        ids.append(email["id"])
    return ids

    
def send_unseen_emails(user, allEmails, newEmailIDs):
    for email in allEmails:
        if email["isSeen"] == "no" and (email["id"] in newEmailIDs):
            text = f"👀From:\n {email['from'].split('<')[0]}\n\n📩Subject:\n {email['subject']}\n\n📃Snippet:\n {email['snippet']}\n📆Date:\n {email['date']}"
            if send_message(user, text).status_code == 200:
                print("Message sent succesfully ", user.chat_ID)
            else:
                print("Message was unsuccesfull ", user.chat_ID)

def user_thread(user):
    while True:
        all_emails = get_all_emails(user)
        if all_emails != None:
            ids = get_email_ids(all_emails)
            newEmailIDs = list(set(ids).difference(set(user.messages_ID)))
            user.messages_ID = ids
            send_unseen_emails(user,all_emails, newEmailIDs)
        else:
            user.sign_out()
            resend_captcha(user)
            break

        time.sleep(random.randint(40,80))


def resend_captcha(user):
    captcha_filename = get_captcha(user)
    send_captcha(user,captcha_filename)

if __name__ == '__main__':
    app.run(debug=True)
