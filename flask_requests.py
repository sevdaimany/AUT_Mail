from pickle import GLOBAL
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import  request, jsonify
import requests
import random
import json
import time

app = Flask(__name__)
api = Api(app)

URL = "https://webmail.aut.ac.ir"
checkIn = False
KEY = "5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw"
info = {"database":[]}

@app.route('/driver', methods=["POST"])
def start():
    userinfo = request.json
    USERNAME = userinfo["username"]
    PASS = userinfo["password"]
    chatID = userinfo["chatid"]
    
    print("chatID,    ", chatID)
    
    info["username"] = USERNAME
    info["password"] = PASS
    
    #Get captcha from webmail
    rand = str(random.randint(1,10000))
    r1 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=isRequired&username={USERNAME}")
    r2 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=show&username={USERNAME}")
    info["captcha_id"] = r2.headers['Set-Cookie'].split(";")[0].split("=")[1]
    info["chat_id"] = chatID
    file = open(f"{rand}.png", "wb")
    file.write(r2.content)
    file.close()

    #Send captcha to bot
    data = {"chat_id": chatID}
    url = "https://api.telegram.org/bot5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw/sendPhoto" 
    with open(f"{rand}.png", "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
     
    send_message("Please Enter the captcha")   
    return "DONE", 200
  
  
def get_all_emails():
    data = {
    "action":"login",
    "username":info["username"],
    "password": info["password"],
    "captchaId":info["captcha_id"],
    "captchaText":info["captcha_text"]
    
    }
    
    login = requests.post("https://webmail.aut.ac.ir/", data=data)
    if "Set-Cookie" in dict(login.headers).keys():
        send_message("I GOT WRONG INFO!")
        send_message("/newInfo - to correct your inforamtion")
        return "None"
    else:
        print('header', login.headers)
        h = login.text[-230:].split('src="')[1].split("&")[0]
        print("h    ," ,h)
        hmail = login.history[0].headers["Set-Cookie"].split(";")[0].split("=")[1]
        print("hmail    ,", hmail)
        rebuiltCookie = f"passwordExpireWarning=true;displayMoreContent=false;theme=breeze;readingPane=east;_hmail={hmail};_captchaid={info['captcha_id']};public_language=en"
        header = {"cookie": rebuiltCookie, "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}  
        payload = {"folderId":"84729550_134979500", "start":0, "limit":50, "sort":"receivedDateUTC", "dir":"DESC", "operation":"MailList"} 
        url = "https://webmail.aut.ac.ir/api/mail/list" + h
        login = requests.post(url, data=payload, headers=header)
        print("login.text    ,", login.text[:150])
        
        returned = "{" + '"MailObject" :' +  login.text[112:] 
        returned = json.loads(returned)
        allEmails = returned["MailObject"]
        print("all Emails 0 :   " ,allEmails[0])
        return allEmails
        

def send_message(text):
    f = requests.post("https://api.telegram.org/bot5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw/sendMessage" ,json={
            'chat_id':info["chat_id"],
            'text':text,
            })

def get_email_ids(allEmails):
    
    ids = []
    for email in allEmails:
        ids.append(email["id"])
    return ids

    
def send_unseen_emails(allEmails, newEmailIDs):
    for email in allEmails:
        if email["isSeen"] == "no" and (email["id"] in newEmailIDs):
            text = f"From : {email['from']}\nSubject : {email['subject']}\nSnippet : {email['snippet']}\nDate: {email['date']}"
            send_message(text)

def send_emails():
    global info
    all_emails = get_all_emails()
    if all_emails !="None":
        ids = get_email_ids(all_emails)
        newEmailIDs = list(set(ids).difference(set(info["database"])))
        info["database"] = ids
        send_unseen_emails(all_emails, newEmailIDs)
    
    
      
@app.route('/captcha', methods=["POST"])
def captcha():
    captcha_input = request.json["captcha"]
    info["captcha_text"] = captcha_input
    send_emails()
    return captcha_input, 200



if __name__ == '__main__':
    app.run(debug=True)
