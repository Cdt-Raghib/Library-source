from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import StringProperty
from utils.book import Books
from kivymd.uix.dialog import MDDialog
"""
    Merge with other screens
    Add refresh
"""

Builder.load_file('kivymd/book_card_view.kv')
Builder.load_file('kivymd/books.kv')
Builder.load_file('kivymd/book-detail-dialog.kv')

class BookDetailDialog(MDDialog):
    text = StringProperty()
    book_dict = {}
    manager = None

    def load_text(self):
        print('bdd: ', self.book_dict)
        state = 'available' if self.book_dict['stock']>0 else 'unavailable'
        color = 'dc143c' if state=='unavailable' else '20ff08'
        comments = ''#ff9900
        rating = 'unrated' if not self.book_dict['average_rating'] else self.book_dict['average_rating']

        if self.book_dict['comments'] is not None:
            for f in self.book_dict['comments']:
                comments+=f['comment']+'\n'
                comments+=f'[color=ff9900]->{f['cadet_no']}[/color]\n\n'

        self.text = f"""
        [b]About:[/b]\n
        {self.book_dict['title']}\n
        Book no. : {self.book_dict['book_no']}\n
        Author   : {self.book_dict['author']}\n
        Donted by: {self.book_dict['donated_by']}\n
        Status   : [color={color}]{state}[/color]\n
        Rating   : {rating}
        \n
        [b]Comments:[/b]\n
        {comments}
        """
        print(self.text)

    def move_to_issue(self):
        self.dismiss()
        self.manager.root.ids.screen_manager.current = 'issue_books'
        self.manager.app_screens_layout[3].set_book_no(self.book_dict['book_no'])


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
        self.running_app = kwargs.get('main')
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
        'text':'Title',
        'on_release':lambda x='title', y='Title':self.search_by(x,y),
        },
        {
        'text':'Book no.',
        'on_release':lambda x='book_no', y='Book no.':self.search_by(x,y),
        },
        {
        'text':'Author',
        'on_release':lambda x='author', y='Author':self.search_by(x,y),
        }
        ]
        self.options = MDDropdownMenu(items = self.items, caller=caller, position='bottom', theme_bg_color='Custom',
                                      md_bg_color='orange')
        self.options.open()
    
    def init_book_cards(self, find='', search=False):
        rows = self.books.search(self.keyword, find) if search \
        else self.books.get_all(show_error=False)
        print(f'home: {rows}')
        if len(self.ids.boxlayout.children)>1:
            self.ids.boxlayout.remove_widget(self.ids.boxlayout.children[0])
            self.main_view.remove_widget(self.main_view.clear_widgets())
            self.book_layout.clear_widgets()

        for f in rows:
            print(f)
            self.card_view = BookCardView(on_release=lambda y, x=f:self.show_details(book_dict=x))
        
            if f.get('icon', 'e') != 'e':
                self.card_view.icon = f.get('icon')
            self.card_view.text = f.get('title')
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
    
    def show_details(self, book_dict):
        dial = BookDetailDialog()
        dial.manager = self.running_app
        dial.book_dict = book_dict
        dial.load_text()
        dial.open()

    def search(self, text):
        if text.text=='':
            self.init_book_cards()
            return
        
        self.init_book_cards(search=True, find=text)
        

