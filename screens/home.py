from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from utils.book import Books
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.divider import MDDivider

from utils.notificationbar import NotificationBar
"""
    Add refresh: Done
    ***Take all book cards into a RecycleLayout: Done
    ***Optionally remove background
    Dialog view upgraded.
"""

Builder.load_file('kivymd/books.kv')
Builder.load_file('kivymd/book-detail-dialog.kv')

class BookDetailDialog(MDDialog):
    text = StringProperty()
    book_dict = ObjectProperty(dict({'title':'None'}))
    manager = None
    database = None

    def load_info(self):
        state = 'Available' if self.book_dict['stock']>0 else 'Unavailable'
        color = 'dc143c' if state=='Unavailable' else '20ff08'
        acolor = 'ff6e00'
        text1 = f"""
[color={acolor}]{self.book_dict['author']}[/color]
Book no : {self.book_dict['book_no']}
Category: {self.book_dict['category']}
[color={color}]{state}[/color]
        """

        about = f"""
[b]About:[/b]\n{self.book_dict['comments']}
        """
        stars = MDBoxLayout(adaptive_height=True)
        rating = float(self.book_dict['average_rating']/2.)
        for f in range(5):
            if f < int(rating):
                img_src = 'assets/img/star-filled.png'
            elif f < rating:
                if rating-f>=0.5:
                    img_src = 'assets/img/star-half-filled.png'
                else:
                    img_src = 'assets/img/star-unfilled.png'
            else:
                img_src = 'assets/img/star-unfilled.png'
            stars.add_widget(FitImage(source=img_src, size=(58,58), size_hint=(None, None)))
        stars.add_widget(MDLabel(text=f'{rating}/5', bold=True, adaptive_height=True))
        self.ids.info_box.add_widget(MDLabel(text=text1, markup=True, adaptive_height=True))
        self.ids.info_box.add_widget(MDDivider(theme_divider_color='Custom', color=self.theme_cls.primaryColor))
        self.ids.info_box.add_widget(stars)
        self.ids.info_box.add_widget(MDDivider(theme_divider_color='Custom', color=self.theme_cls.primaryColor))
        self.ids.info_box.add_widget(MDLabel(text=about, markup=True, adaptive_height=True))

    def move_to_issue(self):
        self.dismiss()
        self.manager.root.ids.screen_manager.current = 'issue_books'
        self.manager.app_screens_layout[1].set_book_no(self.book_dict['book_no'])

    def move_to_edit(self):
        self.dismiss()
        if self.manager.current_account not in ('admin', 'coadmin'):
            NotificationBar().open_with_text(text='Permission denied', error=True)
            return
        self.manager.hidden_screen_layouts['editor'].move_to_edit('book_no', {'book_no':self.book_dict['book_no']}, 
            database=self.database, table='books')

class BookCardView(MDCard):
    icon = StringProperty('book-open-page-variant')
    text = StringProperty('')
    status = StringProperty()


class Home(MDScreen):
    keyword = 'book_no'
    book_data = ListProperty([])
    _database = None
    card_view = None
    total = StringProperty()
    excess = StringProperty()

    def app_request(self, **kwargs):
        self._database = kwargs.get('databases', None).get('library.db')
        self.running_app = kwargs.get('main')
        if self._database is None:
            raise ValueError("Database not found. Please provide a valid database instance.")

        self.load_books()
        self.init_book_cards()
    
    def refresh(self, **kwargs):
        self.init_book_cards()

    def load_books(self):
        """
        book loader:
            Books will be loaded from database(SQL) files.
        """
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
                                      md_bg_color='blue')
        self.options.open()
    
    def mount_wids(self, rows):
        if rows is None:
            self.book_data = []

        elif len(rows) == 0:
            self.book_data = []
        else:
            self.book_data = []
            for f in rows:
                self.book_data.append(
                    {
                    'text':f.get('title'),
                    'status': 'Available' if f.get('stock')>0 else 'Unavailable',
                    'on_release': lambda x=f:self.show_details(book_dict=x)
                    })
        self.excess = ''
            
    def init_book_cards(self, dt=None, find='', search=False):
        rows = self.books.search(self.keyword, find) if search \
        else self.books.get_all(show_error=False)

        self.total = f'Total: {len(rows)}'
        self.excess = 'Loading widgets...'
        self.mount_wids(rows)

    def search_by(self, keyword, item_text):
        # v.1.1
        self.keyword = keyword
        self.ids.option_button_text.text = item_text
        self.options.dismiss()
    
    def show_details(self, book_dict):
        dial = BookDetailDialog()
        dial.manager = self.running_app
        dial.book_dict = book_dict
        dial.database = self._database
        dial.load_info()
        dial.open()

    def search(self, text):
        if text=='':
            #self.searching_clock = Clock.schedule_once(self.init_book_cards)
            self.init_book_cards()
            return
        
        #self.searching_clock = Clock.schedule_once(lambda dt, x=True, y=text:self.init_book_cards(search=x, find=y))
        self.init_book_cards(search=True, find=text)
        