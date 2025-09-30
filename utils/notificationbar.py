from kivy.lang import Builder
from kivymd.uix.snackbar import MDSnackbar

from kivy.properties import StringProperty


Builder.load_file("kivymd/notification-bar.kv")


class NotificationBar(MDSnackbar):
    text = StringProperty()
    color = StringProperty("green")
    button_text = StringProperty()

    def play_sound(self):
        pass

    def action(self):
        print("Help clicked!")

    def open_with_text(self, text, error=False):
        self.text = text
        
        if error:
            self.button_text = 'Help'
            self.color = 'red'
            
        else:
            self.button_text = ''
            self.color = "green"

        self.open()
