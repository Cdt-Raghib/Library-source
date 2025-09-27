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
    database = None
    
    def app_request(self, **kwargs):
        self.database = kwargs.get('db2')
    
    def load_info(self):
        rows = self.database.fetchall('SELECT username, password FROM accounts')
        if isinstance(rows, int):
            return
        for row in rows:
            row = dict(row)
            self.accounts.append(row['username'])
            self.passwords.append(row['password'])  

    def login(self, username, password):
        self.load_info()
        for f,k in zip(self.accounts,self.passwords):
            print(f,k)
            if username.text == Cipher().decode(f) and password.text == Cipher().decode(k):
                self.manager.current = 'home'#'home'
                self.manager.login_state = True
                return 
            
        self.login_error = True
        self.login_message = "Error Username or Password"

if __name__=='__main__':
    print(Cipher().decode('ehqmr2veklmf'))
    print(Cipher().encode('pyrlibrary@2224'))
    print(Cipher().encode('coadmin.library'))
    print(Cipher().encode('coadmin@library'))
    print(Cipher().encode('asst.library'))
    print(Cipher().encode('i am a volunteer'))