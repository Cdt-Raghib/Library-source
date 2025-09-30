from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
'''
Features to be added:
    on enter move to next filed
'''
Builder.load_file('kivymd/register.kv')

class RegisterUser(MDScreen):
    database = None

    def app_request(self, **kwargs):
        self.database = kwargs.get('db1')
    
    def refresh(self, **kwargs):
        pass

    def register_user(self):
        info = {
            'name': self.ids.name_register.text,
            'cadet_no': self.ids.cadet_no_register.text,
            'batch': self.ids.batch_register.text
        
        }
        result = self.database.execute('INSERT INTO users (cadet_name, cadet_no, batch) VALUES (:name, :cadet_no, :batch)', info, on_error='Error code <ec>: Invalid data or user already exists')
        if isinstance(result, int):
            return
        self.database.commit()
