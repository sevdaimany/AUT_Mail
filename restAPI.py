
from concurrent.futures import thread
import re
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import  request, jsonify


from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
import requests

app = Flask(__name__)
api = Api(app)

PATH_TO_DRIVER = '../SeleniumDrivers/chromedriver.exe'
url = "https://webmail.aut.ac.ir"
checkIn = False
KEY = "5480186611:AAExiA_7Pu6j9lYwsSbE7atcddZThEbw8Sw"





@app.route('/driver', methods=['POST'])
def start():
    driver = webdriver.Chrome(executable_path=PATH_TO_DRIVER, thread=True)
    driver.get(url)

    userinfo = request.json
    USERNAME = userinfo["username"]
    PASS = userinfo["password"]
    chatID = userinfo["chatid"]
    username = driver.find_element("id","username")
    password = driver.find_element("id","password")
    username.clear()
    password.clear()
    username.send_keys(USERNAME)
    password.send_keys(PASS)
    rand = str(random.randint(1,10000))
    
    get_captcha(rand, driver)
    r = requests.post(f"https://api.telegram.org/bot{KEY}" ,json={
    'method':'sendPhoto',
    'chat_id':chatID,
    'photo':open(f"{rand}.png", "rb"),
    })
    
    f = requests.post(f"https://api.telegram.org/bot{KEY}" ,json={
    'method':'sendMessage',
    'chat_id':chatID,
    'text':"Please the captcha",
    })
    return f"{f}", 200
    

@app.route('/captcha', methods=['POST'])
def captcha():
    captcha_input = jsonify(request.json)["captcha"]
    print(captcha_input)
    
def get_captcha(name, driver):
    time.sleep(5)
    captcha = driver.find_element(by=By.XPATH ,value='//*[@id="captcha-img"]')
    captcha.screenshot(f"{name}.png")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
