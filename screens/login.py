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
    
class Login(MDScreen):
    login_message = StringProperty()
    login_error = BooleanProperty(False)
    accounts = []
    passwords = []
    roles = []
    database = None
    main = None
    
    def app_request(self, **kwargs):
        self.database = kwargs.get('databases').get('accounts.db')
        self.main = kwargs.get('main')
    
    def refresh(self, **kwargs):
        pass
    
    def load_info(self):
        rows = self.database.fetchall('SELECT username, password, role FROM accounts')
        if isinstance(rows, int):
            return
        for row in rows:
            row = dict(row)
            self.accounts.append(row['username'])
            self.passwords.append(row['password'])
            self.roles.append(row['role'])
    
    def move_next(self, inst):
        fields = self.children[0].children[2:4]
        print('login.py: ', fields)
        if inst in fields:
            idx = fields.index(inst)
            if idx - 1 >= 0:
                fields[idx - 1].focus = True
            else:
                self.login(self.ids.username, self.ids.password)
                

    def login(self, username, password):
        self.load_info()
        for f,k,z in zip(self.accounts,self.passwords,self.roles):
            print(f,k)
            if username.text == Cipher().decode(f) and password.text == Cipher().decode(k):
                self.main.current_account = z
                self.manager.current = 'home'#'home'
                self.manager.login_state = True
                return 
            
        self.login_error = True
        self.login_message = "Error Username or Password"

if __name__=='__main__':
    print(Cipher().encode('SBH'))
    print(Cipher().encode('987654321'))