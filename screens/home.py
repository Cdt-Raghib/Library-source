from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import StringProperty
from utils.book import Books
"""
    Merge with other screens
"""

Builder.load_file('kivymd/book_card_view.kv')
Builder.load_file('kivymd/books.kv')

class BookCardView(MDCard):
    icon = StringProperty('book-open-page-variant')
    text = StringProperty('')
    # function = ObjectProperty()

class BookList(MDScreen):
    keyword = 'book_no'
    book_inst = []
    _database = None
    card_view = None

    def app_request(self, **kwargs):
        self._database = kwargs.get('db1', None)
        if self._database is None:
            raise ValueError("Database not found. Please provide a valid database instance.")

        self.load_books()
        self.init_book_cards()
    
    def load_books(self):
        """
        book loader:
            Books will be loaded from database(SQL) files.
        """

        self.book_layout = MDStackLayout(orientation= 'lr-tb', spacing='15dp')
        self.main_view = MDScrollView(do_scroll_x=False, scroll_distance='10dp', scroll_wheel_distance='20dp')
        self.books = Books(self._database)        

    def open_options(self, caller):
        self.items = [ 
        {
        'text':'Book name',
        'on_release':lambda x='book_name', y='Book name':self.search_by(x,y),
        },
        {
        'text':'Book no.',
        'on_release':lambda x='book_no', y='Book no.':self.search_by(x,y),
        },
        {
        'text':'Writer name',
        'on_release':lambda x='writer_name', y='Writer name':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom',
                                      md_bg_color='orange')
        self.options.open()
    
    def init_book_cards(self, find='', search=False):
        for f in self.book_inst:
            print(f.dictonary, f.get('icon'))
            if search:
                if not(find in f.get(self.keyword)):
                    continue
            self.card_view = BookCardView(on_relese=lambda x=f:self.show_details(book_inst=x))
            if f.get('icon') != 'Unknown':
                self.card_view.icon = f.get('icon')
            self.card_view.text = f.get('name')
            self.book_layout.add_widget(self.card_view)
        
        self.main_view.add_widget(self.book_layout)
        self.ids.boxlayout.add_widget(self.main_view)

    def search_by(self, keyword, item_text):
        # v.1.1
        self.keyword = keyword
        self.ids.option_button_text.text = item_text
        self.options.dismiss()
    # def search_by(self, keyword, item_text):
    #     v.1.0
    #     self.keyword = keyword
    #     self.ids.item_text.text = item_text
    #     self.options.dismiss()
    
    def show_details(self, inst, book_inst):
        print('Yet to work on')

    def search(self, text):
        if text.text=='':
            self.main_view.remove_widget()
            self.init_book_cards()
            return
        
        self.main_view.remove_widget()
        self.init_book_cards(search=True, find=text)
        
# class TestApp(MDApp):
#     def build(self):
#         return 
    
#     def on_start(self):
        

# if __name__=='__main__':
#     TestApp().run()

