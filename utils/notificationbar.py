from kivy.lang import Builder
from kivymd.uix.snackbar import MDSnackbar
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader

from utils.pathhelper import resource_path
import webbrowser
import os

Builder.load_file(("kivymd/notification-bar.kv"))


class NotificationBar(MDSnackbar):
    text = StringProperty()
    color = StringProperty("green")
    button_text = StringProperty()
    headline = StringProperty()

    def play_sound(self):
        s = SoundLoader.load(('assets/audio/error-sound.mp3'))
        if s:
            s.play()
        
    def action(self):
        file_path = resource_path("assets/data/help.html")
        webbrowser.open(f"file://{file_path}")

    def open_with_text(self, text, error=False):
        self.text = text
        
        if error:
            self.button_text = 'Help'
            self.color = 'red'
            self.headline = 'Error'
            self.play_sound()
            
        else:
            self.button_text = ''
            self.color = "green"
            self.headline = 'Info'

        self.open()
