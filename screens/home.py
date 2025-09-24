from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import StringProperty, ObjectProperty

"""
    Merge with other screens
"""
class Book:
    """
        Later use it globally
    """
    dictonary = {}
    keys = ['book_no', 'icon', 'name', 'writer_name', 'donated_by', 'average_rating','comments']
    def __init__(self, **book_info):
        self.dictonary = book_info
    
    def __init__(self, book_info:list):
        splitted_info = book_info.split('|')

        for k,f in zip(self.keys,splitted_info):
            self.dictonary[k] = f
    
    def _decode(self, text):
        if '[bn]' in text:
            pass
            # end with [/bn]|Pyavro required
        text = text.replace('[n]', '\n')
        return text

    def _encode(self, text):
        text.replace('\n', '[n]')

    def get(self, key):
        request = self.dictonary.get(key, 'Unknown')
        if request == '':
            request = 'Unknown'
        print(request, type(request))
        return self._decode(request)
    
    def set(self, key, value):
        if not(key in self.keys):
            raise f"Unknown option: {key}. Permitted options are: {self.keys}"
        
        self.dictonary[key] = self._encode(value)

"""
Sequence:
    [book no.|icon|name|writer's name|donated by|average rating|comments(use [n] instead of \n)|]
"""
Builder.load_file('kivymd/book_card_view.kv')

class BookCardView(MDCard):
    icon = StringProperty('book-open-page-variant')
    text = StringProperty('')
    # function = ObjectProperty()

class BookList(MDScreen):
    keyword = 'book_no'
    book_inst = []
    card_view = None

    def app_request(self, **kwargs):
        pass
    
    def load_books(self):
        """
        book loader:
            Books will be loaded from JSON or database(SQL) files in further update.
        """
        # For test only usage
        self.book_layout = MDStackLayout(orientation= 'lr-tb', spacing='15dp')
        self.main_view = MDScrollView(do_scroll_x=False, scroll_distance='10dp', scroll_wheel_distance='20dp')
        data_path = 'assests/data/books.txt'
        with open(data_path, 'r', encoding='utf-8') as file:
            self.all_books = file.read().split('\n')

        for f in self.all_books:
            self.book_inst.append(Book(f))

    def open_options(self, caller):
        self.items = [ #may create an issue
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
        
class TestApp(MDApp):
    def build(self):
        return Builder.load_file('kivymd/books.kv')
    
    def on_start(self):
        self.root.load_books()
        self.root.init_book_cards()

if __name__=='__main__':
    TestApp().run()

