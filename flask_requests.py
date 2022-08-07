from flask import Flask
from flask_restful import  Api
from flask import  request
import requests
import random
import json
from apscheduler.schedulers.background import BackgroundScheduler

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
    
    info["username"] = USERNAME
    info["password"] = PASS
    
    #Get captcha from webmail
    rand = str(random.randint(1,10000))
    r1 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=isRequired&username={USERNAME}")
    r2 = requests.get(f"https://webmail.aut.ac.ir/captcha.hsp?action=show&username={USERNAME}")
    info["captcha_id"] = r2.headers['Set-Cookie'].split(";")[0].split("=")[1]
    info["chat_id"] = chatID
    file = open(f"./captcha/{rand}.png", "wb")
    file.write(r2.content)
    file.close()

    #Send captcha to bot
    data = {"chat_id": chatID}
    url = "https://api.telegram.org/bot5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw/sendPhoto" 
    with open(f"./captcha/{rand}.png", "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
     
    send_message("Please Enter the captcha")   
    return "DONE", 200

 
    
      
@app.route('/captcha', methods=["POST"])
def captcha():
    captcha_input = request.json["captcha"]
    info["captcha_text"] = captcha_input
    send_emails()
    return captcha_input, 200

  
def get_all_emails():
    login = requests.post(info["url"], data=info["payload"], headers=info["header"])
    returned = "{" + '"MailObject" :' +  login.text[112:] 
    returned = json.loads(returned)
    allEmails = returned["MailObject"]
    return allEmails
  
def login():
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
        h = login.text[-230:].split('src="')[1].split("&")[0]
        hmail = login.history[0].headers["Set-Cookie"].split(";")[0].split("=")[1]
        rebuiltCookie = f"passwordExpireWarning=true;displayMoreContent=false;theme=breeze;readingPane=east;_hmail={hmail};_captchaid={info['captcha_id']};public_language=en"
        header = {"cookie": rebuiltCookie, "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}  
        payload = {"folderId":"84729550_134979500", "start":0, "limit":50, "sort":"receivedDateUTC", "dir":"DESC", "operation":"MailList"} 
        url = "https://webmail.aut.ac.ir/api/mail/list" + h
        info["url"] = url
        info["payload"] = payload
        info["header"] = header
        return "Done"


    

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
    status= login()
    if status !="None":
        all_emails = get_all_emails()
        ids = get_email_ids(all_emails)
        newEmailIDs = list(set(ids).difference(set(info["database"])))
        info["database"] = ids
        send_unseen_emails(all_emails, newEmailIDs)
        scheduler.start()


def check_for_new_email():
    all_emails = get_all_emails()
    ids = get_email_ids(all_emails)
    newEmailIDs = list(set(ids).difference(set(info["database"])))
    info["database"] = ids
    send_unseen_emails(all_emails, newEmailIDs)


scheduler = BackgroundScheduler()
job = scheduler.add_job(check_for_new_email, 'interval', minutes=5)   
    

if __name__ == '__main__':
    app.run(debug=True)
