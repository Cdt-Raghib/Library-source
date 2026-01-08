from kivymd.uix.screenmanager import MDScreenManager
from kivy.properties import BooleanProperty

dev_check = None
with open('config', 'r') as file:
    dev_check = file.read()
class Skeleton(MDScreenManager):
    login_state = BooleanProperty(dev_check=='d8102224')
