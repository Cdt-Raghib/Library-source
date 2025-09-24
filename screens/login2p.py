from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.screen import MDScreen

Builder.load_file('kivymd/login2.kv')

class Cipher:
    to_ascii_map = {}
    
    def __init__(self):
        self.enMapAscii()

    def enMapAscii(self):
        for f in range(0,256):
            self.to_ascii_map[chr(f)] = f

    def encode(self, text:str):
        encrypted = ''
        for f in text:
            encrypted+=chr(self.to_ascii_map[f]+4)
        
        return encrypted
    
    def decode(self, text):
        decrypted = ''
        for f in text:
            decrypted+=chr(self.to_ascii_map[f]-4)
        
        return decrypted
    
class LoginScreen(MDScreen):
    login_message = StringProperty()
    login_error = BooleanProperty(False)
    accounts = []
    passwords = []
    
    def app_request(self, **kwargs):
        pass
    
    def load_info(self, file_path):
        with open(file_path) as file:
            all = file.read().split('\n')
            self.accounts = all[0].split(' ')
            self.passwords = all[1].split(' ')

    def login(self, username, password):
        self.load_info('assests/data/user_info')
        for f,k in zip(self.accounts,self.passwords):
            print(f,k)
            if username.text == Cipher().decode(f) and password.text == Cipher().decode(k):
                self.manager.current = 'issue_books'#'home'
                self.manager.login_state = True
                return 
            
        self.login_error = True
        self.login_message = "Error Username or Password"

if __name__=='__main__':
    print(Cipher().decode('ehqmr2veklmf'))