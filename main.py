from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem,MDNavigationDrawerItemLeadingIcon,MDNavigationDrawerItemText, MDNavigationDrawerDivider
from kivy.lang import Builder
from kivy.properties import BooleanProperty 

from screens.login import LoginScreen
from screens.add_books import AddBooks
from screens.register import RegisterUser
from screens.issue_books import IssueBooks
from screens.deposit import DepositScreen
from screens.issue_list import IssueList
from screens.home import BookList

from utils.databasemanager import DatabaseManager

"""
version: 2.0.1.1
Goal:
    Add navigation items from python file: Done
    Keep request of children :)
    Create two database library.db and login.db
    Make a database manager class
"""

librarydb = DatabaseManager('assets/databases/library.db')
accountdb = DatabaseManager('assets/databases/accounts.db')
librarydb.executescript('SQL/library.sql')
accountdb.executescript('SQL/accounts.sql')

class MainApp(MDApp):
    app_screens1 = {
        'Home':'home',
        'Issue Books':'book-arrow-up-outline',
        'Deposit Books': 'book-arrow-down-outline',
        'Add Books':'book-plus-outline',
        }

    app_screens2 = {
        'Register User':'account-plus-outline',
        'Settings':'cog'
    }
    def build(self):
        self.theme_cls.primary_palette = "Blue"       # Royal Blue for buttons, accents
        self.theme_cls.primary_hue = "500"
        self.theme_cls.secondary_palette = "Gray"     # For secondary UI elements
        self.theme_cls.accent_palette = "Crimson"
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_color = (0.25, 0.41, 0.88, 1)   # Royal Blue
        self.theme_cls.secondary_color = (0.44, 0.5, 0.56, 1)  # Slate Gray
        self.theme_cls.accent_color = (0.86, 0.08, 0.24, 1)    # Crimson Red
        self.theme_cls.text_color = (0.2, 0.2, 0.2, 1) 

        return Builder.load_file('kivymd/skeleton.kv')
    
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
        self.app_screens_layout = [
            LoginScreen(name='login'),
            AddBooks(name='add_books'),
            RegisterUser(name='register_user'),
            IssueBooks(name='issue_books'),
            DepositScreen(name='deposit_books'),
            IssueList(name='issue_list'),
            BookList(name='home')
        ]
        # self.app_screens_layout[4].ids.tab.switch_tab(text=self.app_screens_layout[4].ids.text1.text)
        self.add_nav_item(self.app_screens1)
        self.root.ids.nav_drawer_menu.add_widget(MDNavigationDrawerDivider())
        self.add_nav_item(self.app_screens2)

        for f in self.app_screens_layout:
            f.md_bg_color = self.theme_cls.transparentColor
            f.app_request(instance=self, db1=librarydb, db2=accountdb)
            self.root.ids.screen_manager.add_widget(f)
        
        self.root.ids.screen_manager.current = 'login'

    def set_screen(self, name):
        self.root.ids.screen_manager.current = self.screenify(name)

    def screenify(self, name:str):
        s = name.lower()
        s = s.replace(' ', '_')
        return s
    
MainApp().run()