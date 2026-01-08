from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import( 
    MDNavigationDrawerItem,
    MDNavigationDrawerItemLeadingIcon,
    MDNavigationDrawerItemText, 
    MDNavigationDrawerDivider,
)
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import os

from utils.databasemanager import DatabaseMaster
from utils.notificationbar import NotificationBar

import importlib
import json

"""
version: main-2.0.1.1
Goal:
    Change the db path to appdata/local: pending
"""

databases = DatabaseMaster({
    'assets/databases/library.db':'SQL/library.sql',
    'assets/databases/accounts.db':'SQL/accounts.sql',
    'assets/databases/history.db': 'SQL/history.sql'
                            })
backupdir = os.environ['LOCALAPPDATA']+'/HouseLibrary/backup/'

dev_check = None
with open('config', 'r') as file:
    dev_check = file.read()
DEV_MODE = dev_check=='d8102224'
UNDER_DEV = ['Settings', 'SQL Console']
os.makedirs(f'{backupdir}', exist_ok=True)

class MainApp(MDApp):
    current_account = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"       # Royal Blue for buttons
        self.theme_cls.primary_hue = "500"
        self.theme_cls.secondary_palette = "Gray"   
        self.theme_cls.accent_palette = "Crimson"
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_color = (0.25, 0.41, 0.88, 1)   # Royal Blue
        self.theme_cls.secondary_color = (0.44, 0.5, 0.56, 1)  # Slate Gray
        self.theme_cls.accent_color = (0.86, 0.08, 0.24, 1)    # Crimson Red
        #self.theme_cls.text_color = (0.2, 0.2, 0.2, 1) 

        #kv_path = os.path.join(base_dir, 'kivymd', 'skeleton.kv')
        #print(f"Loading KV file from: {kv_path}")
        return Builder.load_file('kivymd/skeleton.kv')#kv_path)
    
    def add_nav_item(self, screen_dict):
        for name, icon in screen_dict.items():
            self.root.ids.nav_drawer_menu.add_widget(MDNavigationDrawerItem(
                MDNavigationDrawerItemText(
                    text=name,
                    valign='center',
                ),
                MDNavigationDrawerItemLeadingIcon(
                    icon=icon,
                    pos_hint={'center_y':0.5}
                    
                ),
                on_release=lambda x,y=name:self.set_screen(name=y),
                #fixed: get the instance, control dynamically
                ),
            )

    def on_start(self):
        with open('assets/data/screens.json', 'r') as f:
            self.screen_definitions = json.load(f)

        with open('assets/data/ignorescreens.json') as file:
            self.ignore_screens = json.load(file)

        with open('assets/data/hiddenscreens.json') as file:
            self.hidden_screens = json.load(file) #[module name, screen name]

        self.hidden_screen_layouts = {}

        for module_name, screen_name in self.hidden_screens:
            module = importlib.import_module(f'screens.{module_name}')
            class_name = ''.join(word.title() for word in module_name.split('_'))
            screen_class = getattr(module, class_name)

            screen_inst = screen_class(name=screen_name)
            screen_inst.md_bg_color = self.theme_cls.transparentColor
            screen_inst.app_request(main=self, databases=databases)

            self.hidden_screen_layouts[screen_name] = screen_inst
            self.root.ids.screen_manager.add_widget(screen_inst)

        self.app_screens_layout = []

        for display_name, icon, module_name in self.screen_definitions:
            if display_name == "":
                self.root.ids.nav_drawer_menu.add_widget(MDNavigationDrawerDivider())
                continue

            if display_name in self.ignore_screens:
                continue

            self.add_nav_item({display_name: icon})
            if display_name in UNDER_DEV:
                continue
            module = importlib.import_module(f'screens.{module_name}')
            class_name = ''.join(word.title() for word in module_name.split('_'))
            screen_class = getattr(module, class_name)

            screen_inst = screen_class(name=self.screenify(display_name))
            screen_inst.md_bg_color = self.theme_cls.transparentColor
            screen_inst.app_request(main=self, databases=databases)

            self.app_screens_layout.append(screen_inst)
            self.root.ids.screen_manager.add_widget(screen_inst)
        
        self.root.ids.screen_manager.current = 'login'
        if DEV_MODE:
            MDDialog(
                MDDialogHeadlineText(text='Message'),
                MDDialogSupportingText(text='This is a development version, only for test. Do not use it for keeping records.')
            ).open()

    def set_screen(self, name):
        self.root.ids.nav_drawer.set_state('close')
        if name in UNDER_DEV:
            NotificationBar().open_with_text(text="Under development!", error=True)
            return
        self.root.ids.screen_manager.current = self.screenify(name)

    def screenify(self, name:str):
        s = name.lower()
        s = s.replace(' ', '_')
        return s
    
    def refresh(self):
        s = SoundLoader.load('assets/audio/iced-magic.mp3')
        s.play()
        self.root.ids.screen_manager.current_screen.refresh(main=self)
    
    def on_stop(self):
        databases.commit_all()
        databases.backup_all(backup_folder=backupdir)
        databases.close_all()

if __name__ == '__main__':
    MainApp().run()