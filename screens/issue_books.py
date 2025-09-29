from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from utils.book import Books

'''
Feature to be added:
    add a seperator before cadet no.: Done
    add something to understand screen is scrollable: Done
    add the book if not found with a confirmation dialog: Pending
    Debug it: ...
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
    
    def set_book_no(self, book_no):
        self.ids.book_no.text = str(book_no)
        
    def rectify(self, key):
        key = key.lower()
        key = key.replace(' ', '_')
        key = key.replace('.', '')
        return key
    
    def fetch_info(self):
        for f in self.children[0].children[0].children:
            if f.__class__.__name__ == "ITextField":
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
        r2 = self.database.execute('UPDATE books SET stock=(stock-1) WHERE book_no=?', (self.input_info['book_no'], ), on_error='<ec>:Failed to update stock.')
        if isinstance(r, int) or isinstance(r2, int):
            return False
        ch = self.books.get(int(self.input_info['book_no']), 'title, author, category', on_error='Book not found. Check book no. or add book', show_error=True)
        if isinstance(ch, int):
            return False

        r3 = self.database.execute('SELECT token FROM users WHERE cadet_no=?', (self.input_info['cadet_no'],), on_error='Cannot take more than 2 books.')
        if isinstance(r3, int):
            return False
        tokens = r3.fetchone()['token']
        if tokens<=0:
            return False
        return True
    
    def issue_book(self):
        self.fetch_info()
        print(self.input_info)
        if not self.check_validity():
            return
        columns = ''
        placeholders = ''
        for key, value in self.input_info.items():
            columns += f'{key}, '
            placeholders += f'{value}, '
        columns = columns[:-2]
        placeholders = placeholders[:-2]
        query = f'INSERT INTO transactions ({columns}) VALUES ({placeholders});'
        result = self.database.execute(query, on_error='<ec>:Failed to issue book.')
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
        self.issue_cadet_name = ''
        book = self.books.get(int(book_no.text), 'title, author, category', show_error=False)
        if isinstance(book, int) or book=='':
            return
        if len(book) == 0:
            return
        
        #May create an issue
        self.ids.book_name.text= book['title']
        self.ids.author.text = book['author']
        self.ids.category.text = book['category']

    def search(self, cadet_no):
        result = self.database.execute('SELECT cadet_name, batch FROM users WHERE cadet_no=?', (int(cadet_no.text),), show_error=False)
        if not isinstance(result, int):
            row = result.fetchone()
            if row:
                self.issue_cadet_name = f'Name : {row['cadet_name']}'
                self.issue_cadet_batch = f'Batch: {row['batch']}'
            else:
                self.issue_cadet_name = 'User not found'
                self.issue_cadet_batch = ''