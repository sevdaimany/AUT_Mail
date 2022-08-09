class User:

    def __init__(self, username, password, chat_ID):
        self.username = username
        self.password = password
        self.chat_ID = chat_ID
        self.messages_ID = []
        self.isLoggedIn = False
        self.captcha_text = None
        self.captcha_id = None
        self.url = None
        self.payload = None
        self.header = None


    def sign_out(self):
        self.isLoggedIn = False
        self.captcha_text = None
        self.url = None
        self.captcha_id = None
        self.payload = None
        self.header = None
