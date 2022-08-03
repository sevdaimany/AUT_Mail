
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
from bs4 import BeautifulSoup as bs
import requests
import json


class scraping:

    PATH_TO_DRIVER = './SeleniumDrivers/chromedriver.exe'
    url = "https://webmail.aut.ac.ir"
    
    
    def __init__(self, USERNAME, PASS):
        
        self.driver = webdriver.Chrome(executable_path=self.PATH_TO_DRIVER)
        self.driver.get(self.url)
        self.USERNAME=USERNAME
        self.PASS = PASS
        

    def fill_captcha(self, captcha_input):
        captcha = self.driver.find_element("id", "captchaText")
        login = self.driver.find_element("id", "ext-comp-1008")
        while True:
            r = requests.get(""some url)
            if len(r.text) != 0:
                captcha.send_keys(captcha_input)
                login.click()
                break
            time.sleep(2)
        # captcha.send_keys(captcha_input)
        # login.click()
  
  
    def get_cookie():
        rebuiltCookie = ""
        for cookie in driver.get_cookies():
            rebuiltCookie += cookie["name"]
            rebuiltCookie += "="
            rebuiltCookie += cookie["value"] +";"
        return rebuiltCookie

    
    def get_captcha(self,name):
        time.sleep(5)
        captcha = self.driver.find_element(by=By.XPATH ,value='//*[@id="captcha-img"]')
        captcha.screenshot(f"{name}.png")
    
    def get_email_ids(allEmails):   
        ids = []
        for email in allEmails:
            ids.append(email["id"])
        return ids
     
    
    def get_emails():
        time.sleep(10)
        currURL = "https://webmail.aut.ac.ir/api/mail/list" + driver.current_url.split("/")[-1]
        rebuiltCookie = get_cookie() 
        header = {"cookie": rebuiltCookie, "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        payload = {"folderId":"84729550_134979500", "start":0, "limit":50, "sort":"receivedDateUTC", "dir":"DESC", "operation":"MailList"}       
        r = requests.post(currURL, headers=header, data=payload)
        
        returned = "{" + '"MailObject" :' +  r.text[112:] 
        returned = json.loads(returned)
        allEmails = returned["MailObject"]
        return allEmails
    
