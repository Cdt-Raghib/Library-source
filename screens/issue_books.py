from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from utils.book import Books
from utils.notificationbar import NotificationBar
import sqlite3
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
    
    def refresh(self, **kwargs):
        pass
    
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
                if self.rectify(f.hint_text) in ('cadet_no', 'book_no'):
                    self.input_info[self.rectify(f.hint_text)] = f.text

    def move_next(self, inst):
        fields = [f for f in self.children[0].children[0].children if f.__class__.__name__ == "ITextField"]
        if inst in fields:
            idx = fields.index(inst)
            if idx + 1 < len(fields):
                fields[idx + 1].focus = True
    
    def check_validity(self):
        cadet_no = self.input_info.get('cadet_no')
        book_no = self.input_info.get('book_no')

        if not cadet_no or not book_no:
            NotificationBar().open_with_text(text='Fill all required fields', error=True)
            return False
        
        r = self.database.fetchone('SELECT cadet_no FROM users WHERE cadet_no=?;', (self.input_info['cadet_no'],))
        match r:
            case int():
                return False
            case None:
                NotificationBar().open_with_text(text='User not found', error=True)
                return False
            
        r2 = self.database.fetchone('SELECT stock FROM books WHERE book_no=?', (self.input_info['book_no'], ), on_error='<ec>:Failed to get stock.')
        match r2:
            case None:
                NotificationBar().open_with_text(text='Book not found', error=True)
                return False
            case sqlite3.Row():
                if int(r2['stock'])<=0:
                    NotificationBar().open_with_text(text='Book is out of stock', error=True)
                    return False
            case int():
                return False 

        r4 = self.database.fetchone('SELECT token FROM users WHERE cadet_no=?', (self.input_info['cadet_no'],))
        match r4:
            case int():
                return False
            case sqlite3.Row():
                if int(r4['token'])<=0:
                    NotificationBar().open_with_text(text='Cannot take more than 2 books', error=True)
                    return False
            case None:
                return False
            
        return True
    
    def issue_book(self):
        self.fetch_info()
        print(self.input_info)
        if not self.check_validity():
            return
        columns = ', '.join(self.input_info.keys())
        placeholders = ', '.join(['?'] * len(self.input_info))
        query = f'INSERT INTO transactions ({columns}) VALUES ({placeholders});'
        values = tuple(self.input_info.values())
        result = self.database.execute(query, values, on_error='<ec>:Failed to issue book.')
        
        if isinstance(result, int):
            return
        cut_token = self.database.execute('UPDATE users SET token=token-1 WHERE cadet_no=?', (self.input_info['cadet_no'],), on_error='<ec>:Failed to update token.')
        self.database.execute(
            'UPDATE books SET stock=stock-1 WHERE book_no=?',
            (self.input_info['book_no'],),
            on_error='<ec>:Failed to update stock.'
        )
        if not (isinstance(result, int) or isinstance(cut_token, int)):
            NotificationBar().open_with_text(text='Issued successfully')
            self.database.commit()
    
    def search_book(self, book_no):
        try:
            book_no_int = int(book_no.text)
        except ValueError:
            self.issue_cadet_name = 'Invalid book no.'
            self.issue_cadet_batch = ''
            return
        self.issue_cadet_name = ''
        book = self.books.get(book_no_int, 'title, author, category', show_error=False)
        if isinstance(book, int) or book=='':
            return
        if len(book) == 0:
            return
        
        #May create an issue
        self.ids.book_name.text= book['title']
        self.ids.author.text = book['author']
        self.ids.category.text = book['category']

    def search(self, cadet_no):
        result = self.database.execute('SELECT cadet_name, batch FROM users WHERE cadet_no=?', (cadet_no.text,), show_error=False)
        if not isinstance(result, int):
            row = result.fetchone()
            if row:
                self.issue_cadet_name = f'Name : {row['cadet_name']}'
                self.issue_cadet_batch = f'Batch: {row['batch']}'
            else:
                self.issue_cadet_name = 'User not found'
                self.issue_cadet_batch = ''
