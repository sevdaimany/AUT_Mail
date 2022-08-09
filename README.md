
# AUTMail Bot

Description: Telegram bot for fetching the newly received emails from Amirkabir University of Technology webmail with some cats presence for sure 🐈

With this bot, you’ll get notified on your telegram whenever a new message pops up.

Meow!

![Logo](https://github.com/sevdaimany/AUT_Mail/blob/master/images/logo.jpeg)


## Installation

For deploying this project, you have to first set up a flask server and then run your telegram bot.


* Installing Flask

```bash
$ pip install Flask
$ pip install flask-restful
$ pip install requests
```


* Installing telebot
This API is tested with Python 3.6-3.10 and Pypy 3. There are two ways to install the library:

Installation using pip (a Python package manager):
```bash
$ pip install pyTelegramBotAPI
```
Installation from source (requires git):
```bash
$ git clone https://github.com/eternnoir/pyTelegramBotAPI.git
$ cd pyTelegramBotAPI
$ python setup.py install
```

or:
```bash
$ pip install git+https://github.com/eternnoir/pyTelegramBotAPI.git
```
It is generally recommended to use the first option.

While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling
```bash
$ pip install pytelegrambotapi --upgrade
```


    
## Run Locally

Clone the project

```bash
  git clone https://github.com/sevdaimany/AUT_Mail.git
```

Go to the project directory

```bash
  cd AUT_Mail
```

Start Flask server

```bash
  python flask_requests.py
```

Run the bot 
```bash
  python bot.py
```

## API Reference
#### Starting the Bot
```http
  POST /driver
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `chat_ID` | `string` | **Required**. Your Telegram chat ID |
| `Username` | `string` | **Required**. Your AUT Username |
| `Password` | `string` | **Required**. Your AUT Password |

#### Sending Captcha to the Server

```http
  POST /captcha
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `chat_ID` | `string` | **Required**. Your Telegram chat ID |
| `captcha_text` | `string` | **Required**. Text of the captcha |




## Screenshots

![App Screenshot](https://github.com/sevdaimany/AUT_Mail/blob/master/images/screenshot1.jpeg)

<p float="left">
  <img src="https://github.com/sevdaimany/AUT_Mail/blob/master/images/screenshot2.jpeg" width="200" />
  <img src="https://github.com/sevdaimany/AUT_Mail/blob/master/images/screenshot3.jpeg" width="200" /> 
</p>



## Authors

- [@sevdaimany](https://github.com/sevdaimany)
- [@Mortrest](https://github.com/Mortrest)

