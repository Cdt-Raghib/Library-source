from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import StringProperty, ObjectProperty

class IssueList(MDScreen):
    issue_data = {}
    searchby = StringProperty('Cadet no')

    def open_options(self, caller):
        self.items = [ #may create an issue
        {
        'text':'Book name',
        'on_release':lambda x='book_name', y='Book name':self.search_by(x,y),
        },
        {
        'text':'Cadet no.',
        'on_release':lambda x='book_no', y='Book no.':self.search_by(x,y),
        },
        {
        'text':'Cadet name',
        'on_release':lambda x='writer_name', y='Writer name':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom',
                                      md_bg_color='orange')
        self.options.open()

    def app_request(self, **kwargs):
        """
            Create a database object in main and pass it to here
        """
        pass
    def search(self, text):
        pass

    def search_by(self, hint, plate_text):
        pass

class TestApp(MDApp):
    def build(self):
        return Builder.load_file('kivymd/issue-list.kv')
    
if __name__ == '__main__':
    TestApp().run()