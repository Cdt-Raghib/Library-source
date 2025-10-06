from kivy.lang import Builder
from kivymd.uix.snackbar import MDSnackbar
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader

import webbrowser
import os

Builder.load_file("kivymd/notification-bar.kv")


class NotificationBar(MDSnackbar):
    text = StringProperty()
    color = StringProperty("green")
    button_text = StringProperty()

    def play_sound(self, error):
        s = SoundLoader.load('assets/audio/error-sound.mp3')
        if s and error:
            s.play()
        
    def action(self):
        file_path = os.path.abspath("assets/data/help.html")
        webbrowser.open(f"file://{file_path}")

    def open_with_text(self, text, error=False):
        self.text = text
        self.play_sound(error)
        if error:
            self.button_text = 'Help'
            self.color = 'red'
            
        else:
            self.button_text = ''
            self.color = "green"

        self.open()
