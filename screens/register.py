from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
'''
Features to be added:
    on enter move to next filed
'''
Builder.load_file('kivymd/register.kv')

class RegisterUser(MDScreen):
    def app_request(self, **kwargs):
        pass
