from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from utils.book import Books

'''
Feature to be added:
    add a seperator before cadet no.: Done
    add something to understand screen is scrollable: Done
    add the book if not found with a confirmation dialog: Pending
'''

Builder.load_file('kivymd/issue.kv')

class IssueBooks(MDScreen):
    issue_cadet_name = StringProperty('')
    issue_cadet_batch = StringProperty('')
    input_info = {}
    database = None

    def app_request(self, **kwargs):
        self.database = kwargs.get('db1', None)
        self.books = Books(self.database)
        if self.database is None:
            raise ValueError('No database provided')
        
    def rectify(self, key):
        key = key.lower()
        key = key.replace(' ', '_')
        key = key.replace('.', '')
        return key
    
    def fetch_info(self):
        for f in self.children[0].children[0].children:
            if isinstance(f, Builder.template('ITextField')):
                self.input_info[self.rectify(f.hint_text)] = f.text

    def move_next(self, inst):
        # self.input_info[self.rectify(inst.hint_text)] = inst.text
        print(self.children[0].children[0].children)
        ind = self.children[0].children[0].children.index(inst)
        print(f'found ind:{ind}')
        if ind!=-1 and ind-1>0:
            self.children[0].children[0].children[ind-1].focus = True
    
    def check_validity(self):
        r = self.database.execute('SELECT cadet_no FROM users WHERE cadet_no=?', (self.input_info['cadet_no'],), on_error='User not found. Register first.')
        r2 = self.database.execute('SELECT stock FROM books WHERE book_no=?', (self.input_info['book_no'],), on_error='Book is out of stock in library.')
        if isinstance(r, int) or isinstance(r2, int):
            return False
        ch = self.books.get(self.input_info['book_no'], 'book_name, author, category', on_error='Book not found. Check book no. or add book', show_error=True)
        if isinstance(ch, int):
            return False

        r3 = self.database.execute('SELECT  token FROM users WHERE cadet_no=?', (self.input_info['cadet_no'],), on_error='Cannot take more than 2 books.')
        if isinstance(r3, int):
            return False
        tokens = r3.fetchone()['token']
        if tokens<=0:
            return False
        return True
    
    def issue_book(self):
        self.fetch_info()
        if not self.check_validity():
            return
        columns = ''
        placeholders = ''
        for key, value in self.input_info.items():
            columns += f'{key}, '
            placeholders += f'{value}, '
        columns = columns[:-2]
        placeholders = placeholders[:-2]

        result = self.database.execute(f'INSERT INTO issued_books ({columns}) VALUES ({placeholders});', on_error='<ec>:Failed to issue book.')
        cut_token = self.database.execute('UPDATE users SET token=token-1 WHERE cadet_no=?', (self.input_info['cadet_no'],), on_error='<ec>:Failed to update token.')
        if not (isinstance(result, int) or isinstance(cut_token, int)):
            self.database.commit()
    
    def search_book(self, book_no):
        try:
            int(book_no.text)
        except ValueError:
            self.issue_cadet_name = 'Invalid book no.'
            self.issue_cadet_batch = ''
            return
        books = self.books.get(int(book_no.text), 'book_name, author, category', show_error=False)
        if len(books) == 0:
            return
        book = books[0]
        #May create an issue
        self.ids.book_no.text= book['book_name']
        self.ids.author.text = book['author']
        self.ids.category.text = book['category']

    def search(self, cadet_no):
        result = self.database.execute('SELECT name, batch FROM users WHERE cadet_no=?', (int(cadet_no.text),), show_error=False)
        if not isinstance(result, int):
            row = result.fetchone()
            if row:
                self.issue_cadet_name = row['name']
                self.issue_cadet_batch = row['batch']
            else:
                self.issue_cadet_name = 'User not found'
                self.issue_cadet_batch = ''